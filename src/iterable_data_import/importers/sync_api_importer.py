import logging
from abc import abstractmethod, ABCMeta
from typing import Optional, List, Dict, Any

from requests import Session, Response

from iterable_data_import import (
    UnsupportedImportActionError,
    UserProfile,
    CustomEvent,
    Purchase,
)
from iterable_data_import.error_recorders.api_error_recorder import (
    ApiErrorRecorder,
    NoOpApiErrorRecorder,
)
from iterable_data_import.import_action import (
    ImportAction,
    UpdateUserProfile,
    TrackCustomEvent,
    TrackPurchase,
)
from iterable_data_import.importers.importer import Importer

API_BASE_URL = "https://api.iterable.com/api"


class IterableRequest(metaclass=ABCMeta):
    """
    Class representing an Iterable API request body
    """

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        return {}


class BulkUserUpdateRequest(IterableRequest):
    """
    Class representing an Iterable bulk user update request body

    See: https://api.iterable.com/api/docs#users_bulkUpdateUser
    """

    def __init__(self, users: List[UserProfile]):
        self.users = users

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the bulk update request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        req_api_dict = {"users": [user.to_api_dict for user in self.users]}
        return req_api_dict


class BulkTrackCustomEventRequest(IterableRequest):
    """
    Class representing an Iterable bulk track custom event request body

    See: https://api.iterable.com/api/docs#events_trackBulk
    """

    def __init__(self, events: List[CustomEvent]):
        self.events = events

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the bulk track custom event request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        req_api_dict = {"events": [event.to_api_dict for event in self.events]}
        return req_api_dict


class TrackPurchaseRequest(IterableRequest):
    """
    Class representing an Iterable track purchase request body

    See: https://api.iterable.com/api/docs#commerce_trackPurchase
    """

    def __init__(self, purchase: Purchase):
        self.purchase = purchase

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Get the track purchase request as a dictionary structured for the Iterable API

        :return: the api request body dictionary
        """
        return self.purchase.to_api_dict


class SyncApiImporter(Importer):
    """
    An import service that sends data to Iterable using a synchronous API client
    """

    def __init__(
        self,
        api_key: str,
        error_recorder: Optional[ApiErrorRecorder] = None,
        api_base_url: str = API_BASE_URL,
        users_per_batch: int = 1000,
        events_per_batch: int = 1000,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        if users_per_batch < 1:
            raise ValueError(
                f"users_per_batch must be greater than 1, {users_per_batch} provided"
            )

        if events_per_batch < 1:
            raise ValueError(
                f"users_per_batch must be greater than 1, {events_per_batch} provided"
            )

        self.api_key = api_key
        self.error_recorder = (
            error_recorder if error_recorder else NoOpApiErrorRecorder()
        )
        self.api_client = SyncApiClient(api_key, api_base_url)
        self.users_per_batch = users_per_batch
        self.users = []
        self.events_per_batch = events_per_batch
        self.events = []
        self._logger = logging.getLogger("importers.SyncApiImportService")

    def handle_actions(self, actions: List[ImportAction]) -> None:
        """
        Handle a list of import actions

        Note that many import actions are batched in order to improve
        throughput. Calling this method may not trigger an immediate write to Iterable. For this
        reason it's important to call [[SyncApiImporter.shutdown]] when the import is complete.

        :param actions: list of import actions
        :return: none
        """
        for action in actions:
            self._logger.debug(f"handling import action {action}")
            if isinstance(action, UpdateUserProfile):
                if len(self.users) < self.users_per_batch:
                    self.users.append(action.user)
                else:
                    bulk_update_req = BulkUserUpdateRequest(self.users)
                    res = self.api_client.bulk_update_users(bulk_update_req)
                    self._handle_error(bulk_update_req, res)
                    self.users = []

            elif isinstance(action, TrackCustomEvent):
                if len(self.events) < self.events_per_batch:
                    self.events.append(action.event)
                else:
                    bulk_track_req = BulkTrackCustomEventRequest(self.events)
                    res = self.api_client.bulk_track_events(bulk_track_req)
                    self._handle_error(bulk_track_req, res)
                    self.events = []

            elif isinstance(action, TrackPurchase):
                track_purchase_req = TrackPurchaseRequest(action.purchase)
                res = self.api_client.track_purchase(track_purchase_req)
                self._handle_error(track_purchase_req, res)

            else:
                raise UnsupportedImportActionError(
                    f"{action} is not a supported import action"
                )

    def _handle_error(self, request: IterableRequest, response: Response) -> None:
        if response.status_code >= 400:
            self.error_recorder.record(
                response.status_code, response.text, request.to_api_dict
            )

    def shutdown(self) -> None:
        """
        Send the batches of requests that hadn't reached full capacity yet. __Important__: this
        method must be called before terminating the import or it may not complete successfully.

        :return: none
        """
        self._logger.debug("starting shutdown...")
        if len(self.users) > 0:
            bulk_update_req = BulkUserUpdateRequest(self.users)
            res = self.api_client.bulk_update_users(bulk_update_req)
            self._handle_error(bulk_update_req, res)

        if len(self.events) > 0:
            bulk_track_req = BulkTrackCustomEventRequest(self.events)
            res = self.api_client.bulk_track_events(bulk_track_req)
            self._handle_error(bulk_track_req, res)

        self._logger.debug("shutdown complete")


class SyncApiClient:
    """
    Synchronous client for the Iterable API
    """

    def __init__(
        self, api_key: str, base_url: str, timeout: int = 10, max_retries: int = 5
    ) -> None:
        if timeout <= 0:
            raise ValueError(f"timeout must be greater than 0, {timeout} provided")

        if max_retries <= 0:
            raise ValueError(
                f"max_retries must be greater than 0, {max_retries} provided"
            )

        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

        self.session = Session()
        self.session.headers.update({"Api-Key": self.api_key})

        self._logger = logging.getLogger("importers.SyncApiClient")

    def bulk_update_users(self, req: BulkUserUpdateRequest) -> Response:
        url = f"{self.base_url}/users/bulkUpdate"
        data = req.to_api_dict
        response = self.make_request(url, data)
        return response

    def bulk_track_events(self, req: BulkTrackCustomEventRequest) -> Response:
        url = f"{self.base_url}/events/trackBulk"
        data = req.to_api_dict
        response = self.make_request(url, data)
        return response

    def track_purchase(self, req: TrackPurchaseRequest) -> Response:
        url = f"{self.base_url}/commerce/trackPurchase"
        data = req.to_api_dict
        response = self.make_request(url, data)
        return response

    def make_request(self, url: str, data: Dict[str, Any]) -> Response:
        # TODO - add retries
        self._logger.debug(f"making request {url} {data}")
        response = self.session.post(url, json=data)
        self._logger.debug(f"got response {url} {response.status_code} {response.text}")
        return response

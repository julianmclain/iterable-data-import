import logging
from typing import List

import requests

from iterable_data_import.errors import UnsupportedImportActionError
from iterable_data_import.error_recorders.api_error_recorder import (
    ApiErrorRecorder,
)
from iterable_data_import.import_action import (
    ImportAction,
    UpdateUserProfile,
    TrackCustomEvent,
    TrackPurchase,
)
from iterable_data_import.importers.importer import Importer
from iterable_data_import.importers.iterable_request import (
    BulkUserUpdateRequest,
    BulkTrackCustomEventRequest,
    TrackPurchaseRequest,
    IterableRequest,
)
from iterable_data_import.importers.sync_api_client import SyncApiClient


class SyncApiImporter(Importer):
    """
    An import service that sends data to Iterable using a synchronous API client
    """

    def __init__(
        self,
        api_client: SyncApiClient,
        error_recorder: ApiErrorRecorder,
        users_per_batch: int = 1000,
        events_per_batch: int = 1000,
    ) -> None:
        if not api_client:
            raise ValueError("api_client is required")

        if not error_recorder:
            raise ValueError("error_recorder is required")

        if users_per_batch < 1:
            raise ValueError(
                f"users_per_batch must be greater than or equal to 1, {users_per_batch} provided"
            )

        if events_per_batch < 1:
            raise ValueError(
                f"users_per_batch must be greater than or equal to 1, {events_per_batch} provided"
            )

        self.api_client = api_client
        self.error_recorder = error_recorder
        self.users_per_batch = users_per_batch
        self.users = []
        self.events_per_batch = events_per_batch
        self.events = []
        self._logger = logging.getLogger("importers.SyncApiImportService")

    def handle_actions(self, actions: List[ImportAction]) -> None:
        """
        Handle a list of import actions

        Note that many import actions are batched in order to improve throughput. Calling
        this method may not trigger an immediate write to Iterable. For this reason it's
        important to call [[SyncApiImporter.shutdown]] when the import is complete.

        :param actions: list of import actions
        :return: none
        """
        for action in actions:
            self._logger.debug(f"handling import action {action}")
            if isinstance(action, UpdateUserProfile):
                self._handle_update_user(action)

            elif isinstance(action, TrackCustomEvent):
                self._handle_track_event(action)

            elif isinstance(action, TrackPurchase):
                self._handle_track_purchase(action)

            else:
                # validation in IterableDataImport should prevent this from ever happening
                raise UnsupportedImportActionError(
                    f"{action} is not a supported import action"
                )

    def _handle_update_user(self, action: UpdateUserProfile):
        self.users.append(action.user)
        if len(self.users) >= self.users_per_batch:
            bulk_update_req = BulkUserUpdateRequest(self.users)
            res = self.api_client.bulk_update_users(bulk_update_req)
            self._handle_error(bulk_update_req, res)
            self.users = []

    def _handle_track_event(self, action: TrackCustomEvent):
        self.events.append(action.event)
        if len(self.events) >= self.events_per_batch:
            bulk_track_req = BulkTrackCustomEventRequest(self.events)
            res = self.api_client.bulk_track_events(bulk_track_req)
            self._handle_error(bulk_track_req, res)
            self.events = []

    def _handle_track_purchase(self, action: TrackPurchase):
        track_purchase_req = TrackPurchaseRequest(action.purchase)
        res = self.api_client.track_purchase(track_purchase_req)
        self._handle_error(track_purchase_req, res)

    def _handle_error(
        self, request: IterableRequest, response: requests.Response
    ) -> None:
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

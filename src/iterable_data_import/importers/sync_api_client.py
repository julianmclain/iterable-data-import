import logging

import requests

from iterable_data_import.importers.iterable_request import (
    BulkUserUpdateRequest,
    BulkTrackCustomEventRequest,
    TrackPurchaseRequest,
    IterableRequest,
)

API_BASE_URL = "https://api.iterable.com/api"


class SyncApiClient:
    """
    Synchronous client for the Iterable API
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = API_BASE_URL,
        timeout: int = 10,
        max_retries: int = 5,
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

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount(API_BASE_URL, adapter)
        self.session.headers.update({"Api-Key": self.api_key})

        self._logger = logging.getLogger("importers.SyncApiClient")

    def bulk_update_users(self, req: BulkUserUpdateRequest) -> requests.Response:
        url = f"{self.base_url}/users/bulkUpdate"
        response = self.make_request(url, req)
        return response

    def bulk_track_events(self, req: BulkTrackCustomEventRequest) -> requests.Response:
        url = f"{self.base_url}/events/trackBulk"
        response = self.make_request(url, req)
        return response

    def track_purchase(self, req: TrackPurchaseRequest) -> requests.Response:
        url = f"{self.base_url}/commerce/trackPurchase"
        response = self.make_request(url, req)
        return response

    def make_request(self, url: str, request: IterableRequest) -> requests.Response:
        # TODO - retry logic based on whether the request is idempotent
        # requests doesn't retry if data made it to the server
        # 429 - retry
        # 500, 502, 503, 504 - retry if idempotent
        data = request.to_api_dict
        self._logger.debug(f"making request {url} {data}")
        response = self.session.post(url, json=data, timeout=self.timeout)
        self._logger.debug(f"got response {url} {response.status_code} {response.text}")
        return response

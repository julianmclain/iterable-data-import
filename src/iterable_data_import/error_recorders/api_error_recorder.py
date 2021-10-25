import json
import logging
from pathlib import PurePath
from typing import Dict


class ApiErrorRecorder:
    """
    Abstract base class responsible for recording errors that occur while sending data to the Iterable API

    Errors are persisted as JSON objects with the following keys:
    - response_status
    - response_body
    - request_body
    """

    def record(
        self, response_status: int, response_body: str, request_body: Dict[str, object]
    ) -> None:
        """
        Record a single API error

        :param response_status: the API response HTTP status code
        :param response_body: the API response body
        :param request_body: the request body
        :return: none
        """
        pass


class FileSystemApiErrorRecorder(ApiErrorRecorder):
    """
    An API error recorder that writes errors to the local file system. Errors are persisted
    as newline delimited JSON objects
    """

    def __init__(self, out_file_path: PurePath) -> None:
        self.out_file_path = out_file_path
        self._logger = logging.getLogger(
            "error_recorders.LocalFileSystemApiErrorRecorder"
        )

    def record(
        self, response_status: int, response_body: str, request_body: Dict[str, object]
    ):
        # for now eagerly write errors to the file system in case the program terminates unexpectedly
        with open(self.out_file_path, "a") as f:
            error = _create_error(response_status, response_body, request_body)
            self._logger.debug(f"logging error {error}")
            f.write(json.dumps(error) + "\n")


class NoOpApiErrorRecorder(ApiErrorRecorder):
    """
    An API error recorder that performs no action
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("error_recorders.NoOpApiErrorRecorder")

    def record(
        self, response_status: int, response_body: str, request_body: Dict[str, object]
    ):
        error = _create_error(response_status, response_body, request_body)
        self._logger.debug(f"no op logging error {error}")


def _create_error(
    response_status: int, response_body: str, request_body: Dict[str, object]
):
    error = {
        "response_status": response_status,
        "response_body": response_body,
        "request_body": request_body,
    }
    return error

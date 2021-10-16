import json
import logging
from pathlib import PurePath
from typing import Any, Dict
from abc import ABCMeta, abstractmethod

from iterable_data_import.data_sources.data_source import SourceDataRecord


class MapErrorRecorder(metaclass=ABCMeta):
    """
    Class responsible for recording errors in the function that maps source
    data records to import actions

    Errors are persisted as JSON objects with the following keys:
    - exception
    - data
    """

    @abstractmethod
    def record(self, exception: Exception, data: SourceDataRecord) -> None:
        """
        Record a single map function error

        :param exception: the exception that occurred
        :param data: the source data record passed into the map function
        :return: none
        """
        pass


class FileSystemMapErrorRecorder:
    """
    A map error recorder that writes errors to the local file system. Errors are persisted
    as newline delimited JSON objects.
    """

    def __init__(self, out_file_path: PurePath) -> None:
        self.out_file_path = out_file_path
        self._logger = logging.getLogger(
            "error_recorders.LocalFileSystemMapErrorRecorder"
        )

    def record(self, exception: Exception, data: Dict[str, Any]):
        # for now eagerly write errors to the file system in case the program terminates unexpectedly
        with open(self.out_file_path, "a") as f:
            error = create_error(exception, data)
            self._logger.debug(f"logging error {error}")
            f.write(json.dumps(error) + "\n")


class NoOpMapErrorRecorder:
    """
    A map error recorder that performs no action
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger("error_recorders.NoOpMapErrorRecorder")

    def record(self, exception: Exception, data: Dict[str, Any]):
        error = create_error(exception, data)
        self._logger.debug(f"no op logging error {error}")


def create_error(exception: Exception, data: Dict[str, Any]):
    error = {"exception": exception, "record": data}
    return error

import json
import csv
import logging
from collections.abc import Generator
from pathlib import PurePath

from iterable_data_import import UnsupportedFileFormatError
from iterable_data_import.data_sources.data_source import (
    DataSource,
    FileFormat,
    SourceDataRecord,
)


class FileSystem(DataSource):
    """
    Class responsible for extracting source data records from the local file system

    Note: CSV records are parsed into dictionaries of type Dict[str, str]
    """

    def __init__(self, file_format: FileFormat, file_path: PurePath) -> None:
        self.file_format = file_format
        self.file_path = file_path
        self._logger = logging.getLogger("datasources.FileSystem")
        self.source_data_generator = self._get_generator()

    def __iter__(self):
        return self.source_data_generator

    def __next__(self):
        return next(self.source_data_generator)

    def _get_generator(self) -> Generator[SourceDataRecord, None, None]:
        if self.file_format == FileFormat.CSV:
            with open(self.file_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for record in reader:
                    self._logger.debug(
                        f"reading record from {self.file_path}: {record}"
                    )
                    yield record
        elif self.file_format == FileFormat.NEWLINE_DELIMITED_JSON:
            with open(self.file_path, "r") as f:
                for line in f:
                    self._logger.debug(f"reading line from {self.file_path}: {line}")
                    yield json.loads(line)
        else:
            raise UnsupportedFileFormatError(
                f"{self.file_format} is not a supported file format"
            )

from collections.abc import Iterator
from enum import Enum
from typing import Dict, Any

SourceDataRecord = Dict[str, Any]


class FileFormat(Enum):
    """
    Supported file formats for source data records
    """

    CSV = "csv"
    NEWLINE_DELIMITED_JSON = "newline_delimited_json"


class DataSource(Iterator):
    """
    Iterator over data source records
    """

    def __iter__(self) -> Iterator:
        pass

    def __next__(self) -> SourceDataRecord:
        pass

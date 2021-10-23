import pathlib

from iterable_data_import import (
    IterableDataImport,
    FileFormat,
    ImportAction,
    SourceDataRecord,
)

if __name__ == "__main__":
    api_key = "some_api_key"
    source_path = pathlib.Path(__file__).parent / "data.json"
    source_format = FileFormat.NEWLINE_DELIMITED_JSON
    map_error_out = pathlib.Path(__file__).parent / "map-errors.json"
    api_error_out = pathlib.Path(__file__).parent / "api-errors.json"

    def map_function(record: SourceDataRecord) -> ImportAction:
        raise RuntimeError("This error will be recorded and processing will continue")

    idi = IterableDataImport.create(
        api_key,
        source_path,
        source_format,
        map_error_out,
        api_error_out,
        dry_run=True,
    )
    idi.run(map_function)

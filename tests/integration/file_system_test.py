import pathlib
from iterable_data_import import FileSystem, FileFormat
from .integration_test_utils import (
    generate_csv_file,
    generate_newline_delimited_json_file,
)


def test_read_csv():
    fixture_path = pathlib.Path(__file__).parent / "fixtures" / "fs-data.csv"
    num_records = 10
    generate_csv_file(fixture_path, num_records)

    file_system = FileSystem(fixture_path, FileFormat.CSV)

    seen_count = 0
    for record in file_system:
        seen_count += 1
        assert isinstance(record["id"], str)
        assert isinstance(record["email"], str)
        assert isinstance(record["lifetime_value"], str)
        assert isinstance(record["street_address"], str)
        assert isinstance(record["city"], str)
        assert isinstance(record["state"], str)
        assert isinstance(record["zip"], str)
        assert isinstance(record["loves_pizza"], str)
    assert seen_count == num_records


def test_read_newline_delimited_json():
    fixture_path = pathlib.Path(__file__).parent / "fixtures" / "fs-data.json"
    num_records = 10
    generate_newline_delimited_json_file(fixture_path, num_records)

    file_system = FileSystem(fixture_path, FileFormat.NEWLINE_DELIMITED_JSON)

    seen_count = 0
    for record in file_system:
        seen_count += 1
        assert isinstance(record["id"], int)
        assert isinstance(record["email"], str)
        assert isinstance(record["lifetime_value"], int)
        assert isinstance(record["address"]["street_address"], str)
        assert isinstance(record["address"]["city"], str)
        assert isinstance(record["address"]["state"], str)
        assert isinstance(record["address"]["zip"], str)
        assert isinstance(record["loves_pizza"], bool)
    assert seen_count == num_records

import pathlib
from iterable_data_import import FileSystem, FileFormat


def test_read_csv():
    fixture_path = (
        pathlib.Path(__file__).parent / "fixtures" / "10000-test-csv-records.csv"
    )
    file_format = FileFormat.CSV
    file_system = FileSystem(file_format, fixture_path)

    seen_count = 0
    for record in file_system:
        seen_count += 1
        assert isinstance(record["id"], str)
        assert isinstance(record["email"], str)
        assert isinstance(record["brand_affinity_score"], str)
        assert isinstance(record["street_address"], str)
        assert isinstance(record["city"], str)
        assert isinstance(record["state"], str)
        assert isinstance(record["zip"], str)
        assert isinstance(record["loves_pizza"], str)
    assert seen_count == 10000


def test_read_csv_with_extra_whitespace():
    pass


def test_read_csv_with_extra_fields():
    pass


def test_read_csv_with_missing_fields():
    pass


def test_csv_missing_header_fails():
    pass


def test_read_newline_delimited_json():
    fixture_path = (
        pathlib.Path(__file__).parent
        / "fixtures"
        / "10000-test-newline-delimited-json-records.json"
    )
    file_format = FileFormat.NEWLINE_DELIMITED_JSON
    file_system = FileSystem(file_format, fixture_path)

    seen_count = 0
    for record in file_system:
        seen_count += 1
        assert isinstance(record["id"], int)
        assert isinstance(record["email"], str)
        assert isinstance(record["brand_affinity_score"], int)
        assert isinstance(record["address"]["street_address"], str)
        assert isinstance(record["address"]["city"], str)
        assert isinstance(record["address"]["state"], str)
        assert isinstance(record["address"]["zip"], str)
        assert isinstance(record["loves_pizza"], bool)
    assert seen_count == 10000


def test_invalid_json_format_fails():
    pass


def test_unsupported_format_fails():
    pass


# todo - test for mismatched data (e.g. fileformat csv and data is json)

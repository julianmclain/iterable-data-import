import pathlib
from iterable_data_import import (
    IterableDataImport,
    FileSystem,
    FileFormat,
    UserProfile,
    UpdateUserProfile,
    SyncApiImporter,
)


def test_update_user_local_csv():
    # todo - mock local file system?
    fixture_path = (
        pathlib.Path(__file__).parent / "fixtures" / "10-test-csv-records.csv"
    )
    file_format = FileFormat.CSV
    data_source = FileSystem(file_format, fixture_path)
    importer = SyncApiImporter("api_key")

    def map_function(record):
        email = record["email"]
        user_id = record["id"]
        data_fields = {"score": int(record["brand_affinity_score"])}
        user = UserProfile(email, user_id, data_fields)
        return UpdateUserProfile(user)

    idi = IterableDataImport(data_source, importer, map_function, dry_run=True)
    idi.run()
    # todo - assert no_op_service was called correctly


def test_track_custom_event_local_csv():
    pass


def test_track_purchase_local_csv():
    pass


def test_multi_action_local_csv():
    pass


def test_update_user_local_nd_json():
    # todo - mock local file system
    fixture_path = (
        pathlib.Path(__file__).parent
        / "fixtures"
        / "10-test-newline-delimited-json-records.json"
    )
    file_format = FileFormat.NEWLINE_DELIMITED_JSON
    data_source = FileSystem(file_format, fixture_path)
    importer = SyncApiImporter("api_key")

    def map_fn(record):
        email = record["email"]
        user_id = record["id"]
        data_fields = {"score": record["brand_affinity_score"]}
        user = UserProfile(email, user_id, data_fields)
        return UpdateUserProfile(user)

    idi = IterableDataImport(data_source, importer, map_fn, dry_run=True)
    idi.run()
    # todo: assert no_op_service.handle_action was called with expected values and expected number of times


def test_track_custom_event_local_nd_json():
    pass


def test_track_purchase_local_nd_json():
    pass


def test_multi_action_local_nd_json():
    pass

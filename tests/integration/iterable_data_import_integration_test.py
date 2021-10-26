import dotenv
import os
import pathlib

from .integration_test_utils import (
    IterableApiHelpers,
    generate_csv_file,
    generate_newline_delimited_json_file,
)
from iterable_data_import import (
    IterableDataImport,
    FileFormat,
    UserProfile,
    UpdateUserProfile,
    CustomEvent,
    TrackCustomEvent,
)

dotenv.load_dotenv()
API_KEY = os.getenv("ITERABLE_API_KEY")
itbl_helpers = IterableApiHelpers(API_KEY)


def test_csv_import():
    fixture_path = pathlib.Path(__file__).parent / "fixtures" / "data.csv"
    generate_csv_file(fixture_path, 10)

    def map_function(record):
        email = record["email"]
        user_id = str(record["id"])
        data_fields = {"ltv": record["lifetime_value"]}
        user = UserProfile(email, user_id, data_fields)
        return UpdateUserProfile(user)

    idi = IterableDataImport.create(
        api_key=API_KEY,
        source_file_path=fixture_path,
        source_file_format=FileFormat.CSV,
    )

    idi.run(map_function)
    # TODO - fetch users from Iterable


def test_newline_delimited_json_import():
    fixture_path = pathlib.Path(__file__).parent / "fixtures" / "data.json"
    generate_newline_delimited_json_file(fixture_path, 10)

    def map_function(record):
        email = record["email"]
        user_id = str(record["id"])
        data_fields = {"ltv": int(record["lifetime_value"])}
        user = UserProfile(email, user_id, data_fields)
        event = CustomEvent("Test Event", email, user_id, {"foo_attribute": "bar"})
        return [UpdateUserProfile(user), TrackCustomEvent(event)]

    idi = IterableDataImport.create(
        api_key=API_KEY,
        source_file_path=fixture_path,
        source_file_format=FileFormat.NEWLINE_DELIMITED_JSON,
    )

    idi.run(map_function)
    # TODO - fetch users from Iterable

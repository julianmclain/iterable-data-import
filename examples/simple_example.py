import pathlib

from iterable_data_import import (
    IterableDataImport,
    FileFormat,
    UserProfile,
    ImportAction,
    UpdateUserProfile,
    SourceDataRecord,
)

if __name__ == "__main__":
    source_path = pathlib.Path(__file__).parent / "data.json"
    source_format = FileFormat.NEWLINE_DELIMITED_JSON
    api_key = "some_api_key"

    def map_function(record: SourceDataRecord) -> ImportAction:
        email = record["email"]
        user_id = record["id"]
        data_fields = {"ltv": record["lifetime_value"]}
        user = UserProfile(email, user_id, data_fields)
        return UpdateUserProfile(user)

    idi = IterableDataImport.create(
        api_key, source_path, source_format, map_function, dry_run=True
    )
    idi.run()

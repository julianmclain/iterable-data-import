import pathlib
from iterable_data_import import (
    IterableDataImport,
    FileSystem,
    FileFormat,
    SyncApiImporter,
    UserProfile,
    ImportAction,
    UpdateUserProfile,
    SourceDataRecord,
)

file_path = pathlib.Path(__file__).parent / "data.json"
file_format = FileFormat.NEWLINE_DELIMITED_JSON
data_source = FileSystem(file_format, file_path)
api_importer = SyncApiImporter("some_api_key")


def map_function(record: SourceDataRecord) -> ImportAction:
    email = record["email"]
    user_id = record["id"]
    data_fields = {"score": record["brand_affinity_score"]}
    user = UserProfile(email, user_id, data_fields)
    return UpdateUserProfile(user)


idi = IterableDataImport(data_source, api_importer, map_function, dry_run=True)
idi.run()

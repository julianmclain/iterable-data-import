# import dotenv
# import os
# import pathlib
#
# from .integration_test_utils import (
#     IterableApiHelpers,
#     generate_csv_file,
#     generate_newline_delimited_json_file,
# )
# from iterable_data_import import (
#     IterableDataImport,
#     FileSystem,
#     FileFormat,
#     UserProfile,
#     UpdateUserProfile,
#     SyncApiImporter,
# )
#
# dotenv.load_dotenv()
# API_KEY = os.getenv("ITERABLE_API_KEY")
# itbl_helpers = IterableApiHelpers(API_KEY)
#
#
# def test_import_local_csv():
#     fixture_path = (
#         pathlib.Path(__file__).parent / "fixtures" / "integration-test-data.csv"
#     )
#     generate_csv_file(fixture_path, 10)
#     file_format = FileFormat.CSV
#     source = FileSystem(fixture_path, file_format)
#     import_service = SyncApiImporter(API_KEY)
#
#     def map_function(record):
#         email = record["email"]
#         user_id = record["id"]
#         data_fields = {"score": int(record["brand_affinity_score"])}
#         user = UserProfile(email, user_id, data_fields)
#         return UpdateUserProfile(user)
#
#     idi = IterableDataImport(source, import_service, map_function)
#     idi.run()
#
#     # todo
#     # seen_users = 0
#     # for user in get_csv_users(fixture_path):
#     #     itbl_user = itbl_helpers(user['email'])
#
#
# def test_import_local_nd_json():
#     pass
#
#
# def test_import_with_map_errors():
#     pass
#
#
# def test_import_with_import_errors():
#     pass

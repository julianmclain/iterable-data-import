import pathlib

import pytest
from pytest_mock import MockerFixture
from iterable_data_import import (
    IterableDataImport,
    UserProfile,
    UpdateUserProfile,
    TrackCustomEvent,
    TrackPurchase,
    CustomEvent,
    Purchase,
    CommerceItem,
    FileFormat,
    SourceDataRecord,
    ImportAction,
    FileSystem,
    SyncApiImporter,
    NoOpMapErrorRecorder,
    FileSystemMapErrorRecorder,
    NoOpApiErrorRecorder,
    FileSystemApiErrorRecorder,
    SyncApiClient,
    NoOpImporter,
)


# TODO - make these pytest fixtures
user = UserProfile(email="test@iterable.com")
update_user_action = UpdateUserProfile(user)

event = CustomEvent("test event", email="test@iterable.com")
track_event_action = TrackCustomEvent(event)

commerce_item = CommerceItem("1", "shoes", 99.0, 1)
purchase = Purchase(user, [commerce_item], 99.0)
track_purchase_action = TrackPurchase(purchase)

API_KEY = "some_api_key"
SOURCE_PATH = pathlib.Path(__file__).parent / "data.json"
SOURCE_FORMAT = FileFormat.NEWLINE_DELIMITED_JSON


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (update_user_action, [update_user_action]),
        (track_event_action, [track_event_action]),
        (track_purchase_action, [track_purchase_action]),
        (
            [update_user_action, track_purchase_action, track_event_action],
            [update_user_action, track_purchase_action, track_event_action],
        ),
        (user, []),
        ([user, purchase], []),
        (["random string", 53], []),
    ],
)
def test_get_import_actions(test_input, expected):
    assert IterableDataImport._get_import_actions(test_input) == expected


def test_create_instance():
    idi = IterableDataImport.create(
        API_KEY,
        SOURCE_PATH,
        SOURCE_FORMAT,
    )
    assert isinstance(idi.data_source, FileSystem)
    assert idi.data_source.file_path == SOURCE_PATH
    assert idi.data_source.file_format == SOURCE_FORMAT
    assert isinstance(idi.map_error_recorder, NoOpMapErrorRecorder)
    assert isinstance(idi.importer, SyncApiImporter)
    assert isinstance(idi.importer.error_recorder, NoOpApiErrorRecorder)
    assert isinstance(idi.importer.api_client, SyncApiClient)
    assert idi.importer.api_client.api_key == API_KEY


def test_create_instance_with_dry_run():
    idi = IterableDataImport.create(API_KEY, SOURCE_PATH, SOURCE_FORMAT, dry_run=True)
    assert isinstance(idi.data_source, FileSystem)
    assert idi.data_source.file_path == SOURCE_PATH
    assert idi.data_source.file_format == SOURCE_FORMAT
    assert isinstance(idi.importer, NoOpImporter)


def test_create_instance_with_map_error_recorder():
    error_out = pathlib.Path(__file__).parent / "map-errors.json"
    idi = IterableDataImport.create(
        API_KEY,
        SOURCE_PATH,
        SOURCE_FORMAT,
        map_function_error_out=error_out,
    )
    assert isinstance(idi.map_error_recorder, FileSystemMapErrorRecorder)
    assert idi.map_error_recorder.out_file_path == error_out


def test_create_instance_with_api_error_recorder():
    error_out = pathlib.Path(__file__).parent / "api-errors.json"
    idi = IterableDataImport.create(
        API_KEY, SOURCE_PATH, SOURCE_FORMAT, api_error_out=error_out
    )
    assert isinstance(idi.importer.error_recorder, FileSystemApiErrorRecorder)
    assert idi.importer.error_recorder.out_file_path == error_out


def test_catch_and_record_map_function_exception(mocker: MockerFixture):
    error = ValueError("boom!")

    def bad_fn(record: SourceDataRecord):
        raise error

    idi = IterableDataImport.create(
        API_KEY,
        SOURCE_PATH,
        SOURCE_FORMAT,
    )
    mock_data = ['{"foo": "bar"}\n']
    idi.data_source = mock_data
    spy = mocker.spy(idi.map_error_recorder, "record")
    idi.run(bad_fn)
    spy.assert_called_once_with(error, mock_data[0])


def test_shutdown_called(mocker: MockerFixture):
    idi = IterableDataImport.create(
        API_KEY, SOURCE_PATH, SOURCE_FORMAT, _map_function, dry_run=True
    )
    idi.data_source = ['{"foo": "bar"}\n']
    spy = mocker.spy(idi.importer, "shutdown")
    idi.run(_map_function)
    spy.assert_called_once()


def _map_function(record: SourceDataRecord) -> ImportAction:
    return UpdateUserProfile(UserProfile("test@iterable.com"))

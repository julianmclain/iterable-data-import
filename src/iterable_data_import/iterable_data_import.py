import logging
from pathlib import PurePath
from typing import Callable, List, Optional

from iterable_data_import.import_action import ImportAction
from iterable_data_import.data_sources.data_source import DataSource, FileFormat
from iterable_data_import.data_sources.file_system import FileSystem
from iterable_data_import.error_recorders.api_error_recorder import (
    NoOpApiErrorRecorder,
    FileSystemApiErrorRecorder,
)
from iterable_data_import.error_recorders.map_error_recorder import (
    MapErrorRecorder,
    NoOpMapErrorRecorder,
    FileSystemMapErrorRecorder,
)
from iterable_data_import.importers.importer import Importer
from iterable_data_import.importers.sync_api_importer import SyncApiImporter
from iterable_data_import.importers.no_op_importer import NoOpImporter
from iterable_data_import.importers.sync_api_client import SyncApiClient


class IterableDataImport:
    """
    The primary class of the library. Responsible for orchestrating the import process.
    """

    def __init__(
        self,
        data_source: DataSource,
        importer: Importer,
        map_error_recorder: MapErrorRecorder,
    ) -> None:
        if not data_source:
            raise ValueError('Missing required argument "data_source"')

        if not importer:
            raise ValueError('Missing required argument "importer"')

        if not map_error_recorder:
            raise ValueError('Missing required argument "map_error_recorder"')

        self.map_error_recorder = map_error_recorder
        self.importer = importer
        self.data_source = data_source
        self._logger = logging.getLogger("IterableDataImport")

    def run(self, map_function: Callable) -> bool:
        if not map_function:
            raise ValueError('Missing required argument "map_function"')

        self._logger.info("starting import...")
        count = (
            0  # TODO - track count in DataSource, needed for partial restarts anyways
        )

        for record in self.data_source:
            count += 1
            map_fn_return = None

            try:
                map_fn_return = map_function(record)
            except Exception as e:
                self._logger.error(f"an error occurred processing record {count}: {e}")
                self.map_error_recorder.record(e, record)

            import_actions = self._get_import_actions(map_fn_return)
            self.importer.handle_actions(import_actions)

            if count % 1000 == 0:
                self._logger.info(f"imported {count} records")

        self.importer.shutdown()
        self._logger.info(f"import complete, processed {count} source data records")
        return True

    @staticmethod
    def _get_import_actions(unknown: object) -> List[ImportAction]:
        actions = []
        maybe_actions = unknown if isinstance(unknown, list) else [unknown]
        for obj in maybe_actions:
            if isinstance(obj, ImportAction):
                actions.append(obj)
        return actions

    # TODO - create a builder / factory class
    # TODO - probably better to log errors somewhere by default
    @classmethod
    def create(
        cls,
        api_key: str,
        source_file_path: PurePath,
        source_file_format: FileFormat,
        map_function_error_out: Optional[PurePath] = None,
        api_error_out: Optional[PurePath] = None,
        dry_run: bool = False,
    ) -> "IterableDataImport":
        if not api_key:
            raise ValueError('Missing required argument "api_key"')

        if not source_file_path:
            raise ValueError('Missing required argument "source_file_path"')

        if not source_file_format:
            raise ValueError('Missing required argument "source_file_format"')

        if dry_run:
            importer = NoOpImporter()
        else:
            api_client = SyncApiClient(api_key)
            api_error_recorder = (
                FileSystemApiErrorRecorder(api_error_out)
                if api_error_out
                else NoOpApiErrorRecorder()
            )
            importer = SyncApiImporter(api_client, api_error_recorder)

        map_error_recorder = (
            FileSystemMapErrorRecorder(map_function_error_out)
            if map_function_error_out
            else NoOpMapErrorRecorder()
        )

        source = FileSystem(source_file_path, source_file_format)
        idi = IterableDataImport(source, importer, map_error_recorder)
        return idi

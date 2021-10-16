import logging
from typing import Callable, Optional

from iterable_data_import.data_sources.data_source import DataSource
from iterable_data_import.error_recorders.map_error_recorder import (
    MapErrorRecorder,
    NoOpMapErrorRecorder,
)
from iterable_data_import.importers.importer import Importer
from iterable_data_import.importers.no_op_importer import NoOpImporter


class IterableDataImport:
    """
    The primary class of the library. Responsible for orchestrating the import process.
    """

    def __init__(
        self,
        data_source: DataSource,
        importer: Importer,
        map_function: Callable,
        map_error_recorder: Optional[MapErrorRecorder] = None,
        dry_run: bool = False,
    ) -> None:
        if not data_source:
            raise ValueError('Missing required argument "data_source"')

        if not importer:
            raise ValueError('Missing required argument "importer"')

        if not map_function:
            raise ValueError('Missing required argument "map_function"')

        self.map_error_recorder = (
            map_error_recorder if map_error_recorder else NoOpMapErrorRecorder()
        )
        self.importer = importer if not dry_run else NoOpImporter()
        self.data_source = data_source
        self.map_function = map_function
        self.map_error_recorder = map_error_recorder
        self._logger = logging.getLogger("IterableDataImport")

    def run(self) -> bool:
        self._logger.info("starting import...")
        for count, record in enumerate(self.data_source, 1):
            map_fn_return = None
            try:
                map_fn_return = self.map_function(record)
            except Exception as e:
                self._logger.error(f"an error occurred processing record {count}: {e}")
                self.map_error_recorder.record(e, record)

            if isinstance(map_fn_return, list):
                self.importer.handle_actions(map_fn_return)
            elif map_fn_return is not None:
                self.importer.handle_actions([map_fn_return])

            if count % 1000 == 0:
                self._logger.info(f"imported {count} records")

        self.importer.shutdown()
        self._logger.info("import complete")
        return True

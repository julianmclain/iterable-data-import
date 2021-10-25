import logging
from typing import List

from iterable_data_import.import_action import ImportAction
from iterable_data_import.importers.importer import Importer


class NoOpImporter(Importer):
    """
    An importer that performs no action. Useful for dry runs.
    """

    def __init__(self):
        self._logger = logging.getLogger("importers.NoOpImportService")

    def handle_actions(self, actions: List[ImportAction]) -> None:
        for action in actions:
            self._logger.debug(f"no op handle action {action}")

    def shutdown(self):
        self._logger.debug("shutdown complete")

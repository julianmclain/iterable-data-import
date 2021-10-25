from typing import List

from iterable_data_import.import_action import ImportAction


class Importer:
    """
    Abstract base class responsible for writing data to Iterable
    """

    def handle_actions(self, actions: List[ImportAction]) -> None:
        """
        Handle a list of import actions

        :param actions: list of import actions to be performed
        :return: none
        """
        pass

    def shutdown(self) -> None:
        """
        Perform clean up tasks and shutdown.

        This method must be called after all of the import actions have been
        handled or the import may not complete successfully.

        :return: none
        """
        pass

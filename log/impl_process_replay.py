from log_manager.log_manager import BatchLogManager
from log_manager.typeclass import LoggingOperations

from starcraft_data_orm.operations.config import SessionLocal
from starcraft_data_orm.operations import OperationsBase
from starcraft_data_orm.operations.injection import models

from injection_manager import InjectionManager

class ProcessReplay(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = BatchLogManager(InjectionManager(OperationsBase), SessionLocal))

    def log_pre_action(self, action_name: str, **kwargs):
        """
        Log details before the action begins.
        """
        pass

    def log_post_action_success(self, action_name: str, **kwargs):
        """
        Log details after the action completes successfully.
        """
        pass

    def log_post_action_failure(self, action_name: str, exception: Exception, **kwargs):
        """
        Log details after the action fails.
        """
        pass

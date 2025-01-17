from log_manager.log_manager import BatchLogManager
from log_manager.typeclass.logging_operations import LoggingOperations

from starcraft_data_orm.warehouse.config import SessionLocal
from starcraft_data_orm.warehouse import WarehouseBase
## from starcraft_data_orm.warehouse.injection import models

from injection_manager.managers.InjectionManager import InjectionManager

batch_log_manager = BatchLogManager(InjectionManager(WarehouseBase), SessionLocal)

class LogInjection(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = batch_log_manager

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
        breakpoint()
        pass

class LogDownload(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = batch_log_manager

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
        breakpoint()
        pass

class LogParse(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = batch_log_manager

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
        breakpoint()
        pass

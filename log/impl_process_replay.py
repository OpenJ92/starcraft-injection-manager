from log_manager.log_manager import BatchLogManager
from log_manager.typeclass.logging_operations import LoggingOperations

from starcraft_data_orm.warehouse.config import SessionLocal
from starcraft_data_orm.warehouse import WarehouseBase
## from starcraft_data_orm.warehouse.injection import models

from injection_manager.managers.InjectionManager import InjectionManager

from datetime import datetime

batch_log_manager = BatchLogManager(InjectionManager(WarehouseBase), SessionLocal)

class LogInjection(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = batch_log_manager

    def log_pre_action(self, action_name: str, replay, **kwargs):
        """
        Log details before the action begins.
        """
        #print(f"Start injeciton on {replay.filehash}")
        pass

    def log_post_action_success(self, action_name: str, replay, **kwargs):
        """
        Log details after the action completes successfully.
        """
        #print(f"Complete injeciton on {replay.filehash}")
        pass

    def log_post_action_failure(self, action_name: str, replay, exception: Exception, **kwargs):
        """
        Log details after the action fails.
        """
        #print(f"Fail injeciton on {replay.filehash}")
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
        pass

class LogParse(LoggingOperations):
    def __init__(self):
        self.batch_log_manager = batch_log_manager

    def log_pre_action(self, action_name: str, **kwargs):
        """
        Log details before the action begins.
        """
        # print(f"Start Parsing replay {kwargs.get('replay_path')}")
        pass

    def log_post_action_success(self, action_name: str, **kwargs):
        """
        Log details after the action completes successfully.
        """
        # print(f"Complete Parsing replay {kwargs.get('replay_path')}")
        pass

    def log_post_action_failure(self, action_name: str, exception: Exception, **kwargs):
        """
        Log details after the action fails.
        """
        # print(f"Failed Parsing replay {kwargs.get('replay_path')}")
        pass

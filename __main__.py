from starcraft_injection_manager.BatchInjector import BatchInjector, SyncBatchInjector
from starcraft_data_orm.warehouse.config import SessionLocal, SyncSessionLocal
from starcraft_data_orm.warehouse import initialize_warehouse, WarehouseBase

from storage_bridge.asynchro.local import AsyncLocalStorage

from asyncio import run

import sc2reader
from sc2reader.engine.plugins import (
    SelectionTracker,
    APMTracker,
    ContextLoader,
    GameHeartNormalizer,
)

## sc2reader.engine.register_plugin(SelectionTracker())
## sc2reader.engine.register_plugin(APMTracker())
## sc2reader.engine.register_plugin(ContextLoader())
## sc2reader.engine.register_plugin(GameHeartNormalizer())

async def main():
    import sys

    # Disable printing
    # sys.stdout = open('/dev/null', 'w')

    # Initialize the starcraft_data_orm schema
    print("Initializing starcraft_data_orm...")
    initialize_warehouse()

    import psutil

    num_physical = psutil.cpu_count(logical=False)  # Use for multiprocessing
    num_logical = psutil.cpu_count(logical=True)    # Use for asyncio tasks
    print(num_physical, num_logical)

    num_workers = min(num_physical, 32)  # Limit to a reasonable number

    batch = BatchInjector( WarehouseBase,SessionLocal,AsyncLocalStorage('../external')
                         , max_concurrent_tasks = num_workers-1
                         )
    await batch.inject()

    ## batch = SyncBatchInjector(WarehouseBase,SessionLocal,AsyncLocalStorage('examples'))
    ## await batch.inject()

    # Re-enable printing
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    run(main())

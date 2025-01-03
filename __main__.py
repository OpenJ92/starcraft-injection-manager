from starcraft_injection_manager.BatchInjector import BatchInjector
from starcraft_data_orm.warehouse.config import SessionLocal
from starcraft_data_orm.warehouse import initialize_warehouse, WarehouseBase

from storage_bridge import LocalStorage

import sc2reader
from sc2reader.engine.plugins import (
    SelectionTracker,
    APMTracker,
    ContextLoader,
    GameHeartNormalizer,
)

sc2reader.engine.register_plugin(SelectionTracker())
sc2reader.engine.register_plugin(APMTracker())
sc2reader.engine.register_plugin(ContextLoader())
sc2reader.engine.register_plugin(GameHeartNormalizer())

def main():
    # Initialize the starcraft_data_orm schema
    print("Initializing starcraft_data_orm...")
    initialize_warehouse()

    batch = BatchInjector(WarehouseBase, SessionLocal, LocalStorage('examples'))
    batch.inject()

if __name__ == "__main__":
    main()

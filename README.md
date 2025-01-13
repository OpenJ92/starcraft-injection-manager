## Status: Work in Progress

# Starcraft Injection Manager

**Starcraft Injection Manager** is an async-enabled framework designed for efficient data ingestion and injection into the database as part of the **Starcraft Data Platform**. It leverages SQLAlchemy and the `starcraft-data-orm` library to streamline data workflows, ensuring robust and scalable handling of replay data.

## Features

- **Async Injection Framework**: Handles high-volume data ingestion with modern async Python capabilities.
- **Integration with `starcraft-data-orm`**: Uses prebuilt SQLAlchemy Base objects for seamless ORM integration.
- **Batch Injection**: Supports bulk data processing with tools for managing dependencies between data models.
- **Error Handling**: Implements conflict resolution strategies to address issues like simultaneous insertions and race conditions.
- **Customizable Pipelines**: Flexible architecture allows for tailored injection workflows to meet project-specific requirements.
- **Storage Management**: Integrates with [`storage-bridge`](https://github.com/OpenJ92/storage-bridge) to handle data transfers between local and S3 storage seamlessly.
- **Repository Integration**: Leverages [`injection-manager`](https://github.com/OpenJ92/injection-manager) and [`log-manager`](https://github.com/OpenJ92/log-manager) for managing data workflows and logging operations efficiently within the repository.

## Installation
``` bash
pip install starcraft-injection-manager
```

## Usage

The injection manager is designed to integrate seamlessly into the Starcraft Data Platform workflows. Example usage is provided in the main file.
```python
from starcraft_injection_manager.BatchInjector import BatchInjector
from starcraft_data_orm.warehouse.config import SessionLocal, SyncSessionLocal
from starcraft_data_orm.warehouse import initialize_warehouse, WarehouseBase

from storage_bridge.asynchro.local import AsyncLocalStorage

from asyncio import run

async def main():
    # Initialize the starcraft_data_orm schema
    print("Initializing starcraft_data_orm...")
    initialize_warehouse()

    batch = BatchInjector(WarehouseBase, SessionLocal, AsyncLocalStorage('examples'))
    await batch.inject()

if __name__ == "__main__":
    run(main())
```

## Integration with the Data Platform

The **Starcraft Injection Manager** works seamlessly with other components of the **Starcraft Data Platform**, including:

- **starcraft-data-orm**: Provides SQLAlchemy Base objects and session management.
- **storage-bridge**: Handles data storage.
- **starcraft-gather-manager**: Supplies scraped replay files for processing.

## Development Status

This project is under active development. While stable for core functionality, enhancements and additional features are in progress.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you would like to add new features or report bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

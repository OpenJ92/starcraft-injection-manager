from sc2reader import load_replay
from collections import defaultdict
from asyncio import gather, Semaphore
from sqlalchemy.exc import IntegrityError

from injection_manager.managers.InjectionManager import InjectionManager
from log_manager.db_logger import db_logger
from log.impl_process_replay import LogDownload, LogParse, LogInjection

from starcraft_injection_manager.RetryOn import RetryOn

import traceback
import time
import logging
import random
from asyncio import sleep, run


class BatchInjector:
    """
    The BatchInjector class manages the batch processing and injection of StarCraft II replay files into a database.

    It coordinates downloading replays, preparing them for processing, and injecting their data into the database
    while limiting concurrent tasks to prevent overloading resources.

    Attributes:
        session_factory: A callable that returns an asynchronous database session.
        injector (InjectionManager): Handles the injection of prepared replay data.
        storage: Manages storage operations, including downloading and listing files.
        semaphore (Semaphore): Limits the number of concurrent download and inject tasks.
    """


    def __init__(self, base, session_factory, storage, max_concurrent_tasks=8):
        """
        Initializes the BatchInjector with necessary dependencies.

        Args:
            base: The sqlalchemy base used by the InjectionManager.
            session_factory: A callable that provides an asynchronous sqlalchemy database session.
            storage: A storage handler for managing replay files (e.g., S3 or local storage).
            max_concurrent_tasks (int): The maximum number of concurrent tasks allowed. Default is 8.
        """
        self.session_factory = session_factory
        self.injector = InjectionManager(base)
        self.storage = storage
        self.semaphore = Semaphore(max_concurrent_tasks)  # Limit concurrent download-inject tasks

    async def inject(self):
        """
        Coordinates the batch injection process by listing replay files,
        processing each replay, and managing concurrent tasks.

        Raises:
            Exception: If an unexpected error occurs during the batch injection process.
        """
        try:
            tasks = []
            replay_files = await self.storage.async_list_files()
            random.shuffle(replay_files)

            for replay_file in replay_files[:300]:
                coroutine = self._process_replay(replay_file)
                tasks.append(coroutine)

            results = await gather(*tasks, return_exceptions=True)

        except Exception as e:
            raise e

    @RetryOn((IntegrityError, ))
    async def _process_replay(self, replay_file):
        """
        Processes a single replay file by downloading, loading, preparing,
        and injecting it into the database.

        Args:
            replay_file: The name of the replay file to process.

        Raises:
            ValueError: If the download operation fails to return a valid replay path.
            Exception: For any unexpected errors during the processing or injection stages.
        """
        async with self.semaphore:
            try:
                jitter = random.uniform(0, 0.3)  # 0 to 450 ms
                await sleep(jitter)

                replay_path = await self._download_replay(replay_file=replay_file, storage=self.storage)
                replay = await self._parse_replay(replay_path=replay_path)

                async with self.session_factory() as session:
                    await self._inject_replay(replay=replay, session=session, injector=self.injector)

            except Exception as e:
                error_type = type(e).__name__
                error_message = str(e)
                stack_trace = traceback.format_exc()

                print("Error occurred!")
                print(f"Type: {error_type}")
                ## print(f"Message: {error_message}")
                ## print("Stack Trace:")
                ## print(stack_trace)
                raise e

    @db_logger(action="download", logger=LogDownload())
    async def _download_replay(self, replay_file, storage):
        """
        Downloads a replay file from the storage system.

        Args:
            replay_file (str): The name of the replay file to download.

        Returns:
            str: The local path where the replay file was downloaded.

        Raises:
            ValueError: If the download operation fails and no valid path is returned.
        """

        replay_path = await storage.async_download(replay_file, f'examples/{replay_file}')
        if not replay_path:
            raise ValueError(f"Download failed, no replay path returned for {replay_file}")
        return replay_path

    @db_logger(action="parse", logger=LogParse())
    async def _parse_replay(self, replay_path):
        """
        Parses a replay file into a structured replay object.

        Args:
            replay_path (str): The local file path of the replay to parse.

        Returns:
            Replay: The parsed replay object.

        Raises:
            ValueError: If the replay parsing fails or the resulting replay object is invalid.
        """
        replay = load_replay(replay_path)
        if not replay:
            raise ValueError(f"Failed to parse replay at {replay_path}")
        self._prepare(replay)
        return replay

    @db_logger(action="inject", logger=LogInjection())
    async def _inject_replay(self, replay, session, injector):
        """
        Injects a parsed replay object into the database.

        Args:
            replay (Replay): The parsed replay object to inject.
            session (AsyncSession): The database session used for the injection process.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the database injection process.
        """
        await injector.inject(replay, session)

    def _prepare(self, replay):
        """
        Prepares a replay for injection by transforming its events into a dictionary format.

        Modifies the replay object in place by:
        - Creating a `events_dictionary` attribute to store events grouped by name.
        - Removing the `events` attribute to reduce memory usage.

        Args:
            replay: A replay object loaded by sc2reader.
        """
        replay.events_dictionary = defaultdict(list)

        for event in replay.events:
            replay.events_dictionary[event.name].append(event)

        del replay.events


class SyncBatchInjector(BatchInjector):
    def __init__(self, base, session_factory, storage):
        self.session_factory = session_factory
        self.injector = InjectionManager(base)
        self.storage = storage

    async def inject(self):
        await self.process_all_replays()

    async def process_all_replays(self):
        replay_files = await self.storage.async_list_files()
        for replay_file in replay_files[:300]:
            await self._process_replay(replay_file)

    async def _process_replay(self, replay_file):
        replay_path = await self._download_replay(replay_file=replay_file, storage=self.storage)
        replay = await self._parse_replay(replay_path=replay_path)
        async with self.session_factory() as session:
            await self._inject_replay(replay=replay, session=session, injector=self.injector)



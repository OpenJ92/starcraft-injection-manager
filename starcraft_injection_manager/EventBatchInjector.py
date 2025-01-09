from sc2reader import load_replay
from collections import defaultdict
from asyncio import gather, Semaphore

from injection_manager.managers.EventInjectionManager import EventInjectionManager

class EventBatchInjector:
    def __init__(self, base, session_factory, storage, max_concurrent_tasks=5):
        self.session_factory = session_factory
        self.injector = EventInjectionManager(base)
        self.storage = storage
        self.semaphore = Semaphore(max_concurrent_tasks)  # Limit concurrent download-inject tasks

    async def inject(self):
        replay_files = await self.storage.list_files_async()  # Use async storage method
        tasks = [self._process_replay(replay_file) for replay_file in replay_files]
        await gather(*tasks, return_exceptions=True)  # Handle all replays concurrently

    async def _process_replay(self, replay_file):
        """Handles downloading, preparing, and injecting a single replay."""
        async with self.semaphore:
            # Async download
            replay_path = await self.storage.download_async(replay_file, f'examples/{replay_file}')
            replay = load_replay(replay_path)

            # Prepare replay
            self._prepare(replay)

            # Async injection
            async with self.session_factory() as session:
                await self.injector.inject(replay, session)

    def _prepare(self, replay):
        """Prepare replay by organizing events."""
        replay.events_dictionary = defaultdict(list)
        for event in replay.events:
            replay.events_dictionary[event.name].append(event)
        del replay.events

from sc2reader import load_replay
from collections import defaultdict
from asyncio import gather, Semaphore

from injection_manager.managers.InjectionManager import InjectionManager

class BatchInjector:
    def __init__(self, base, session_factory, storage, max_concurrent_tasks=5):
        self.session_factory = session_factory
        self.injector = InjectionManager(base)
        self.storage = storage
        self.semaphore = Semaphore(max_concurrent_tasks)  # Limit concurrent download-inject tasks

    async def inject(self):
        try:
            tasks = []
            replay_files = await self.storage.async_list_files()

            for replay_file in replay_files:
                coroutine = self._process_replay(replay_file)
                tasks.append(coroutine)

            results = await gather(*tasks, return_exceptions=True)

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def _process_replay(self, replay_file):
        try:
            print(f"Starting download for: {replay_file}")
            replay_path = await self.storage.async_download(replay_file, f'examples/{replay_file}')
            if not replay_path:
                raise ValueError(f"Download failed, no replay path returned for {replay_file}")
            print(f"Downloaded replay to: {replay_path}")

            replay = load_replay(replay_path, load_map=True)
            print(f"Replay loaded: {replay}")

            self._prepare(replay)
            async with self.session_factory() as session:
                await self.injector.inject(replay, session)

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def _prepare(self, replay):
        replay.events_dictionary = defaultdict(list)

        for event in replay.events:
            replay.events_dictionary[event.name].append(event)

        del replay.events


from sc2reader import load_replay

from starcraft_injection_manager.InjectionManager import InjectionManager

class BatchInjector:
    def __init__(self, base, session_factory, storage):
        self.session_factory = session_factory
        self.injector = InjectionManager(base)
        self.storage = storage

    def inject(self):
        with self.session_factory() as session:
            try:
                replay_files, tasks = self.storage.list_files(), []

                for replay_file in replay_files:
                    replay_path = self.storage.download(replay_file, f'examples/{replay_file}')
                    replay = load_replay(replay_path, load_map=True)

                    ## constuct and attach hashmap of events w/event.name
                    self._prepare(replay)

                    self.injector.inject(replay, session)

            except Exception as e:
                print(f"Unexpected error: {e}")
                pass

    def _prepare(self, replay):
        replay.events_dictionary = defaultdict(list)

        for event in replay.events:
            replay.events_dictionary[event.name].append(event)

        del replay.events


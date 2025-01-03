from starcraft_injection_manager.AsyncInjectable import AsyncInjectable

class InjectionManager():
    def __init__(self, base):
        """
        Initialize the InjectionManager.
        :param metadata: SQLAlchemy metadata (Base.metadata).
        """
        self.base = base
        self.metadata = base.metadata
        ## self.sorted_relations = self._topological_sort()


    async def inject(self, replay, session):
        """
        Perform the injection process for a replay.
        :param replay: Parsed replay object to inject.
        :param session: Database session supporting flush, commit and rollback:
        """
        try:
            for relation in self.metadata.sorted_tables:
                name = f"{relation.schema}.{relation.name}"
                relation_cls = self.base.injectable.get(name)
                if relation_cls and issubclass(relation_cls, AsyncInjectable):
                    await relation_cls.process(replay, session)
                    await session.flush()  # Flush after each relation
            await session.commit()  # Commit transaction after all relations

        except Exception as e:
            await session.rollback()
            print(f"Unexpected error: {e}")
            # Gracefully handle all other exceptions

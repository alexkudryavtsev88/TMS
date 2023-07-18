from db_connector import DatabaseConnector


class QueryExecutor:
    def __init__(self):
        self._db_connector = DatabaseConnector()
        self._db_session = self._init_db_session()

    def _init_db_session(self):
        self._db_connector.configure_session()
        return self._db_connector.SESSION

    async def exec_query(self, query):
        async with self._db_session as session:
            async with self._db_session.begin():
                result = await session.execute(query)
                return result

    async def get_scalar_one(self, query):
        result = await self.exec_query(query)
        return result.unique().scalar_one()

    async def get_scalars(self, query):
        result = await self.exec_query(query)
        return result.scalars().all()

    async def get_all(self, query, commit=False):
        result = await self.exec_query(query)
        return result.all()

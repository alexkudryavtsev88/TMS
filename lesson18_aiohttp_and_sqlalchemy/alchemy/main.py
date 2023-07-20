import asyncio

# from db_connector import init_all_connections
from executor import QueryExecutor
from models.user_models import User
from sqlalchemy import text, select, insert, update

executor = QueryExecutor()


async def get_users():
    data = await executor.exec_query(text('SELECT * from users'))

    print(data.all())


if __name__ == "__main__":
    # asyncio.run(init_all_connections())
    asyncio.run(get_users())

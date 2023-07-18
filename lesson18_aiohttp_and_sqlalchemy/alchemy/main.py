import asyncio

from db_connector import init_all_connections
from executor import QueryExecutor
from models.user_models import User
from sqlalchemy import text

executor = QueryExecutor()


# async def get_users():
#     stmt = text("SELECT * FROM users WHERE name=:name")
#     stmt = stmt.bindparams(name="Ann")
#     data = await executor.exec_query(stmt)
#
#     print(data.all())


if __name__ == "__main__":
    asyncio.run(init_all_connections())
    # asyncio.run(get_users())

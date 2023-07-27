import asyncio

from lesson21_client_server_database.client_and_server.client import Client
from lesson21_client_server_database.structures import User


SERVER_PORT = 8000
SERVER_URL = f"http://0.0.0.0:{SERVER_PORT}"


async def main():
    user = User(
        name="Alex",
        age=34,
        gender="male",
    )
    client = Client(server_url=SERVER_URL)
    result = await client.add_post(user, "New Post 3", "I'm a New Post 3!")
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
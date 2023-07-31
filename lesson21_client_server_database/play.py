import asyncio

from lesson21_client_server_database.client_and_server.client import Client
from lesson21_client_server_database.structures import User
from lesson21_client_server_database.client_and_server.config import SERVER_PORT


SERVER_HOST = f"http://0.0.0.0"
SERVER_URL = f"{SERVER_HOST}:{SERVER_PORT}"


async def main():
    client = Client(server_url=SERVER_URL)

    user = User(
        name="Alex",
        age=34,
    )
    post_tile, post_description = f"{user.name} new post", "I love you!"

    # ADD
    add_post_result = await client.add_post(user, post_tile, post_description)
    print(add_post_result)

    add_comment_result = await client.add_comment(user, post_tile, post_description, comment_title="Great Post!")
    print(add_comment_result)

    add_like_result = await client.add_like(user, post_tile, post_description)
    print(add_like_result)

    # DELETE
    delete_post_result = await client.delete_post(user, post_tile, post_description)
    print(delete_post_result)


if __name__ == '__main__':
    asyncio.run(main())
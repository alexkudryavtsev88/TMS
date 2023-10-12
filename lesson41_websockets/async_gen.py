import asyncio
import aiohttp
import aiohttp.web

import typing


_SERVER_URL = "http://0.0.0.0:8001"


async def get_item_from_server() -> typing.AsyncGenerator:
    async with aiohttp.ClientSession() as session:
        for i in range(1, 101):
            async with session.get(f"{_SERVER_URL}/next_item") as resp:
                data = await resp.json()
                yield data


async def main():
    response = get_item_from_server()
    async for item in response:
        print(item)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import aiohttp
import aiohttp.web


_SERVER_URL = "http://0.0.0.0:8001"


async def get_item_from_server():
    async with aiohttp.ClientSession() as session:
        for i in range(1, 101):
            async with session.get(f"{_SERVER_URL}/next_item") as resp:
                resp = await resp.json()
                yield resp


async def main():
    async for item in get_item_from_server():
        print(item)


if __name__ == '__main__':
    asyncio.run(main())
import aiohttp
import asyncio


_SERVER_URL = "http://0.0.0.0:8002"
_WS_ENDPOINT = f"{_SERVER_URL}/ws"


async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)

    await ws.send_str(new_msg_to_send)


async def main():
    session = aiohttp.ClientSession()
    msg_types = {aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR}

    async with session.ws_connect(_WS_ENDPOINT) as ws:
        await prompt_and_send(ws)
        async for msg in ws:
            print('Message received from server:', msg)
            await prompt_and_send(ws)

            if msg.type in msg_types:
                break


if __name__ == '__main__':
    print('Type "exit" to quit')
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    asyncio.run(main())

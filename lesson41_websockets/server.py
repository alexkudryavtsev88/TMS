import asyncio
import logging
import sys
from http import HTTPMethod, HTTPStatus
from aiohttp import WSMsgType

from aiohttp import web, web_request

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
    "[%(name)s:%(funcName)s:%(lineno)s][%(threadName)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


class SimpleServer:

    def __init__(self, port: int = 8000):
        self.name = self.__class__.__name__
        self._port = port
        self._content_type = 'application/json'

        # app
        self._app = web.Application()
        self._app.router.add_route(
            method=HTTPMethod.GET,
            path="/",
            handler=self.check_handle,
        )

    def start(self):
        logger.info(f"Starting the <{self.name}> at port {self._port}")
        web.run_app(self._app, port=self._port)

    @staticmethod
    async def check_handle(_: web_request.Request) -> web.Response:
        return web.Response(text='Test handle')


class StorageServer(SimpleServer):

    def __init__(self, port: int = 8001):
        super().__init__(port=port)
        self._storage = map(str, range(1, 101))

        self._app.router.add_route(
            method=HTTPMethod.GET,
            path="/next_item",
            handler=self.produce_item,
        )

    async def produce_item(self, _: web_request.Request) -> web.Response:
        await asyncio.sleep(1)

        return web.Response(
            status=HTTPStatus.OK,
            text=next(self._storage),
            content_type=self._content_type
        )


class WebSocketServer(SimpleServer):

    def __init__(self, port: int = 8002):
        super().__init__(port=port)
        self._app.router.add_route(
            method=HTTPMethod.GET,
            path="/ws",
            handler=self.ws_handler,
        )

    @staticmethod
    async def ws_handler(request):
        logger.info('Websocket connection starting')
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        logger.info('Websocket connection ready')

        async for msg in ws:
            logger.debug(f"Message received: {msg}")

            if msg.type == WSMsgType.TEXT:
                logger.debug(f"Message data: {msg.data}")

                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(f'Answer to {msg.data}')

        print('Websocket connection closed')
        return ws


_SERVERS = {
    StorageServer.__name__.lower(): StorageServer,
    WebSocketServer.__name__.lower(): WebSocketServer,
}


def main(server_name):
    if not (server_cls := _SERVERS.get(server_name.lower())):
        raise ValueError(f"Invalid server name: {server_name}")

    server_cls().start()


if __name__ == '__main__':
    serv_name = WebSocketServer.__name__
    main(serv_name)

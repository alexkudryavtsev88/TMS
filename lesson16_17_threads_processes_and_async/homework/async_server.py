import asyncio
import json
import multiprocessing

import logging

# import requests
from aiohttp import web, web_request
import http

# from queue import Queue
# from multiprocessing import Queue
# from asyncio import Queue

logger = logging.getLogger(__name__)


class ServerEmulator:

    _QUEUE = asyncio.Queue()

    def __init__(self, port: int):
        self.name = self.__class__.__name__
        self._port = port
        self._threshold = 10
        self._calls_count = 0

        # app
        self._app = web.Application()
        self._app.router.add_route(
            method=http.HTTPMethod.GET,
            path='/hello',
            handler=self.hello,
        )
        # self._app.router.add_route(
        #     method='GET',
        #     path='/hello_world',
        #     handler=self.hello_world,
        # )

    def start(self):
        logger.info(f"Starting the <{self.name}> at port {self._port}")
        web.run_app(self._app, port=self._port)

    # def hello_world(self, _: web_request.Request):
    #     print('Hello world!')
    #
    #     return web.Response(
    #         status=200,
    #         text="Hello world!",
    #         content_type='application/json'
    #     )

    async def hello(self, request: web_request.Request) -> web.Response:
        requestor_name = request.query.get('requestor')

        self._calls_count += 1
        # print(self._calls_count)
        await self._QUEUE.put(self._calls_count)

        if self._calls_count % self._threshold == 0:
            raise web.HTTPInternalServerError(
                reason=f"Call number: {self._calls_count}"
            )

        await asyncio.sleep(1)

        value = await self._QUEUE.get()
        print(f'requestor: {requestor_name}, call count: {value}')

        return web.Response(
            status=200,
            text=json.dumps(
                {
                    "key": requestor_name,
                    "value": value
                }
            ),
            content_type='application/json'
        )


def run_server(port: int = 8000):
    def _inner():
        server = ServerEmulator(port=port)
        server.start()

    proc = multiprocessing.Process(target=_inner)
    proc.start()
    return proc

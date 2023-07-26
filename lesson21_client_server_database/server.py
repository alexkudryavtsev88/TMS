import logging
import sys

from aiohttp import web, web_request
from http import HTTPMethod, HTTPStatus
from lesson21_client_server_database.db.connector import DatabaseConnector
from lesson21_client_server_database.db.config import DB_URL

from typing import Any

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Server:

    def __init__(self, port: int = 8000):
        self.name = self.__class__.__name__
        self._port = port

        # app
        self._app = web.Application()
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path='/post_add',
            handler=self.add_post,
        )
        # self._app.router.add_route(
        #     method='GET',
        #     path='/hello_world',
        #     handler=self.hello_world,
        # )

        # db
        self._db_connector = DatabaseConnector(db_url=DB_URL)

    async def start(self):
        logger.info(f"Starting the <{self.name}> at port {self._port}")
        self._db_connector.connect()
        await self._db_connector.check_db()
        web.run_app(self._app, port=self._port)

    async def add_post(self, request: web_request.Request):
        result = self._db_connector.add_post()

    async def add_comment(self, request: web_request.Request):
        result = self._db_connector.add_comment()

    async def add_like(self, request: web_request.Request):
        result = self._db_connector.add_like()

    # async def edit_post(self, post_title: str, edit_data: dict[str, str]):
    #     pass
    #
    # async def edit_comment(self, comment_title: str):
    #     pass
    #
    # def delete_post(self, post_title: str):
    #     pass
    #
    # def delete_comment(self, comment_title: str):
    #     pass
    #
    # def delete_like(self, post_title: str):
    #     pass
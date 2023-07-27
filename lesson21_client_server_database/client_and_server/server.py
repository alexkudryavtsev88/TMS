import json
import multiprocessing
import time

from aiohttp import web, web_request
from http import HTTPMethod, HTTPStatus
from lesson21_client_server_database.db.connector import DatabaseConnector
from lesson21_client_server_database.db.config import DB_URL
from lesson21_client_server_database.structures import OperationStatus


class UnknownOperationStatusError(Exception):
    """
    raises when DatabaseConnector returns unexpected status
    """


class Server:

    def __init__(self, port: int = 8000):
        self.name = self.__class__.__name__
        self._port = port
        self._content_type = 'application/json'

        # app
        self._app = web.Application()
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path='/post_add',
            handler=self.add_post,
        )
        # self._app.router.add_route(
        #     method=HTTPMethod.POST,
        #     path='/comment_add',
        #     handler=self.add_comment,
        # )
        # self._app.router.add_route(
        #     method=HTTPMethod.POST,
        #     path='/like_add',
        #     handler=self.add_like,
        # )

        # db
        self._db_connector = DatabaseConnector(db_url=DB_URL)

    def start(self):
        print(f"Starting the <{self.name}> at port {self._port}")
        self._db_connector.connect()
        web.run_app(self._app, port=self._port)

    async def add_post(self, request: web_request.Request) -> web.Response:
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]

        operation_status = await self._db_connector.add_post(
            user_name=user_name,
            user_age=user_age,
            post_title=post_title,
            post_description=post_description
        )
        match operation_status:
            case OperationStatus.SUCCESS:
                http_status = HTTPStatus.OK
                message = (
                    f"Post '{post_title}', '{post_description}' successfully "
                    f"added to User {user_name}' (age: {user_age})"
                )
            case OperationStatus.NOT_EXIST:
                http_status = HTTPStatus.NOT_FOUND
                message = (
                    f"Cannot add a Post '{post_title}', '{post_description}' "
                    f"to User {user_name} (age: {user_age}) "
                    f"because this User doesn't exist!"
                )
            case OperationStatus.NOT_UNIQUE:
                http_status = HTTPStatus.FORBIDDEN
                message = (
                    f"Cannot add a Post '{post_title}', '{post_description}' "
                    f"to User {user_name} (age: {user_age}) "
                    f"because this Post is already exist!"
                )
            case _:
                raise UnknownOperationStatusError(f"{operation_status}")

        return web.Response(
            status=http_status,
            text=json.dumps(
                {
                    "operation_status": operation_status.value,
                    "message": message
                }
            ),
            content_type=self._content_type
        )

    async def add_comment(self, request: web_request.Request) -> web.Response:
        # error_msg = (
        #     f"Cannot add a Comment to Post '{post_title}', '{post_description}' "
        #     f"because this Post doesn't exist OR is NOT related to "
        #     f"the User '{user_name}', {user_age}"
        # )
        # result = self._db_connector.add_comment()
        pass

    async def add_like(self, request: web_request.Request) -> web.Response:
        # error_msg = (
        #     f"Cannot add a Like to Post '{post_title}', '{post_description}' "
        #     f"because this Post doesn't exist OR is NOT related to "
        #     f"the User '{user_name}', {user_age}"
        # )
        # result = self._db_connector.add_like()
        pass

    """
    Methods bellow are not implemented yet
    """

    async def edit_post(self, request: web_request.Request):
        pass

    async def edit_comment(self, request: web_request.Request):
        pass

    async def delete_post(self, request: web_request.Request):
        pass

    async def delete_comment(self, request: web_request.Request):
        pass

    async def delete_like(self, request: web_request.Request):
        pass


def run_server(port):
    def _start_server():
        server = Server(port=port)
        server.start()

    proc = multiprocessing.Process(target=_start_server)
    proc.start()
    time.sleep(2)

    return proc


if __name__ == '__main__':
    run_server(8000)

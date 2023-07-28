import http
import json
import multiprocessing
import time

from aiohttp import web, web_request
from http import HTTPMethod, HTTPStatus
from lesson21_client_server_database.db.connector import DatabaseConnector
from lesson21_client_server_database.db.config import DB_URL
from lesson21_client_server_database.structures import OperationStatus
from lesson21_client_server_database.client_and_server.config import SERVER_PORT


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
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path='/comment_add',
            handler=self.add_comment,
        )
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path='/like_add',
            handler=self.add_like,
        )

        # db
        self._db_connector = DatabaseConnector(db_url=DB_URL)

    def start(self):
        print(f"Starting the <{self.name}> at port {self._port}")
        web.run_app(self._app, port=self._port)

    async def add_post(self, request: web_request.Request) -> web.Response:
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]

        # async with self._db_connector as db:
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
                    f"Post '{post_title}', '{post_description}' has been "
                    f" successfully added to User {user_name}' (age: {user_age})"
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

        return self._get_response(http_status, operation_status, message)

    async def add_comment(self, request: web_request.Request) -> web.Response:
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]
        comment_title = data["comment"]

        # async with self._db_connector as db:
        operation_status = await self._db_connector.add_comment(
            user_name=user_name,
            user_age=user_age,
            post_title=post_title,
            post_description=post_description,
            comment_title=comment_title
        )

        match operation_status:
            case OperationStatus.SUCCESS:
                http_status = HTTPStatus.OK
                message = (
                    f"Comment '{comment_title}' has been successfully added"
                    f"to Post '{post_title}', '{post_description}'"
                    f"from User {user_name}' (age: {user_age})"
                )
            case OperationStatus.NOT_EXIST:
                http_status = HTTPStatus.NOT_FOUND
                message = (
                    f"Cannot add a Comment to Post '{post_title}', '{post_description}' "
                    f"because this Post doesn't exist OR is NOT related to "
                    f"the User {user_name}, (age: {user_age})"
                )
            case _:
                raise UnknownOperationStatusError(f"{operation_status}")

        return self._get_response(http_status, operation_status, message)

    async def add_like(self, request: web_request.Request) -> web.Response:
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]

        # async with self._db_connector as db:
        operation_status = await self._db_connector.add_like(
            user_name=user_name,
            user_age=user_age,
            post_title=post_title,
            post_description=post_description,
        )

        match operation_status:
            case OperationStatus.SUCCESS:
                http_status = HTTPStatus.OK
                message = (
                    f"Like has been successfully added"
                    f"to Post '{post_title}', '{post_description}'"
                    f"from User {user_name} (age: {user_age})"
                )
            case OperationStatus.NOT_EXIST:
                http_status = HTTPStatus.NOT_FOUND
                message = (
                    f"Cannot add a Like to Post '{post_title}', '{post_description}' "
                    f"because this Post doesn't exist OR is NOT related to "
                    f"the User {user_name} (age: {user_age})"
                )
            case _:
                raise UnknownOperationStatusError(f"{operation_status}")

        return self._get_response(http_status, operation_status, message)

    def _get_response(
        self,
        http_status: http.HTTPStatus,
        op_status: OperationStatus,
        message: str
    ) -> web.Response:
        return web.Response(
            status=http_status,
            text=json.dumps(
                {
                    "operation_status": op_status.value,
                    "message": message
                }
            ),
            content_type=self._content_type
        )

    # TODO: Implement methods bellow as Homework

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
    run_server(port=SERVER_PORT)

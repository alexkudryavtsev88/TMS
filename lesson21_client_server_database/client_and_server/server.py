import enum
import http
import json

from aiohttp import web, web_request
from http import HTTPMethod, HTTPStatus
from lesson21_client_server_database.db.connector import DatabaseConnector
from lesson21_client_server_database.db.config import DB_URL
from lesson21_client_server_database.structures import OperationStatus
from lesson21_client_server_database.client_and_server.config import SERVER_PORT


class Routes(str, enum):
    POST_ADD = '/post_add'
    # POST_EDIT = ''
    POST_DELETE = '/post_delete'
    COMMENT_ADD = '/comment_add'
    # COMMENT_EDIT = ''
    # COMMENT_DELETE = ''
    LIKE_ADD = '/like_add'
    # LIKE_EDIT = ''
    # LIKE_DElETE = ''


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
        # Routes for ADD
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path=Routes.POST_ADD,
            handler=self.add_post,
        )
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path=Routes.COMMENT_ADD,
            handler=self.add_comment,
        )
        self._app.router.add_route(
            method=HTTPMethod.POST,
            path=Routes.LIKE_ADD,
            handler=self.add_like,
        )
        # Routes for DELETE
        self._app.router.add_route(
            method=HTTPMethod.DELETE,
            path=Routes.POST_DELETE,
            handler=self.delete_post,
        )

        # db
        self._db_connector = DatabaseConnector(db_url=DB_URL)

    def start(self):
        print(f"Starting the <{self.name}> at port {self._port}")
        web.run_app(self._app, port=self._port)

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
        comment_title = data["comment_title"]

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
                    f"to Post '{post_title}', '{post_description}' "
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
                    f"to Post '{post_title}', '{post_description}' "
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

    # TODO: Implement methods bellow as Homework

    async def delete_post(self, request: web_request.Request):
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]

        operation_status = await self._db_connector.delete_post(
            user_name=user_name,
            user_age=user_age,
            post_title=post_title,
            post_description=post_description,
        )
        match operation_status:
            case OperationStatus.SUCCESS:
                http_status = HTTPStatus.OK
                message = (
                    f"Post '{post_title}', '{post_description}' "
                    f"was successfully deleted from "
                    f"User {user_name} (age: {user_age})"
                )
            case OperationStatus.NOT_EXIST:
                http_status = HTTPStatus.NOT_FOUND
                message = (
                    f"Post '{post_title}', '{post_description}' "
                    f"was NOT deleted from "
                    f"User {user_name} (age: {user_age}) "
                    f"because this Post doesn't exist"
                )
            case _:
                raise UnknownOperationStatusError(f"{operation_status}")

        return self._get_response(http_status, operation_status, message)

    async def delete_comment(self, request: web_request.Request):
        pass

    async def delete_like(self, request: web_request.Request):
        pass

    async def edit_post(self, request: web_request.Request):
        data = await request.json()

        user_name = data["user"]["name"]
        user_age = data["user"]["age"]
        post_title = data["post_title"]
        post_description = data["post_description"]
        new_post_title = data["new_post_title"]
        new_post_description = data["new_post_description"]

        result = await self._db_connector.edit_post(
            user_name, user_age, post_title,
            post_description, new_post_title, new_post_description
        )

    async def edit_comment(self, request: web_request.Request):
        pass


def run_server(port):
    Server(port=port).start()


if __name__ == '__main__':
    run_server(port=SERVER_PORT)
    print("Hello world")

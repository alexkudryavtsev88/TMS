import traceback

import aiohttp
import yarl
from http import HTTPMethod, HTTPStatus

from lesson21_client_server_database.structures import User


class ClientRequestError(Exception):
    """
    raises when request fails with non-200 status code
    """

    context: dict = {}

    def __init__(self, **kwargs):
        self.context.update(kwargs)
        message = str(self.context)
        super().__init__(message)


class Client:

    def __init__(self, server_url: str):
        self._server_url = yarl.URL(server_url)
        self._session = aiohttp.ClientSession  # class, not instance

    async def _send_request(self, method: HTTPMethod, url: yarl.URL, data: dict[str, str]):
        async with self._session() as session:
            async with session.request(method, url, json=data) as resp:
                try:
                    resp_data = await resp.json()
                except ValueError as exc:
                    traceback.print_exception(exc)
                    print("Cannot get JSON data from Response!")
                else:
                    if resp.status != HTTPStatus.OK:
                        print(f"Request ended with non-SUCCESS status-code: {resp.status}")

                    return resp_data

    async def add_post(self, user: User, post_title: str, post_description: str):
        url = self._server_url / "post_add"
        data = {
            "user": user.to_dict(),
            "post_title": post_title,
            "post_description": post_description
        }
        return await self._send_request(HTTPMethod.POST, url, data)

    async def add_comment(self, user: User, post_title: str, post_description: str, comment_title: str):
        url = self._server_url / "comment_add"
        data = {
            "user": user.to_dict(),
            "post_title": post_title,
            "post_description": post_description,
            "comment_title": comment_title,
        }
        return await self._send_request(HTTPMethod.POST, url, data)

    async def add_like(self, user: User, post_title: str, post_description: str):
        url = self._server_url / "like_add"
        data = {
            "user": user.to_dict(),
            "post_title": post_title,
            "post_description": post_description,
        }
        return await self._send_request(HTTPMethod.POST, url, data)

    # TODO: Implement methods bellow as Homework

    async def edit_post(
        self,
        user: User,
        post_title: str,
        post_description: str,
        new_post_title: str,
        new_post_description: str
    ):
        """
        Implement this method the same way as methods above!
        """""
        pass

    async def edit_comment(
        self,
        user: User,
        post_title: str,
        post_description: str,
        comment_title: str,
        new_comment_title: str
    ):
        pass

    async def delete_post(
        self,
        user: User,
        post_title: str,
        post_description: str,
    ):
        pass

    async def delete_comment(
        self,
        user: User,
        post_title: str,
        post_description: str,
        comment_title: str
    ):
        pass

    async def delete_like(
        self,
        user: User,
        post_title: str,
        post_description: str
    ):
        pass


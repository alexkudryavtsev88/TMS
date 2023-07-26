from lesson21_client_server_database.structures import User
import aiohttp
import yarl
from http import HTTPMethod


class Client:

    def __init__(self, server_url: str, user: User):
        self._server_url = yarl.URL(server_url)
        self._session = aiohttp.ClientSession()
        self._user = user

    async def _send_request(self, method: HTTPMethod, url: yarl.URL, data: dict[str, str]):
        async with self._session as session:
            async with session.request(method, url, **data) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def add_post(self, post_title: str, post_description: str):
        url = self._server_url / "post_add"
        data = {
            "user": self._user.to_dict(),
            "title": post_title,
            "description": post_description
        }
        return await self._send_request(HTTPMethod.POST, url, data)

    async def add_comment(self, comment_title: str):
        url = self._server_url / "comment_add"
        data = {
            "user": self._user.to_dict(),
            "title": comment_title,
        }
        return await self._send_request(HTTPMethod.POST, url, data)

    async def add_like(self, post_title: str, post_description: str):
        url = self._server_url / "like_add"
        data = {
            "user": self._user.to_dict(),
            "post_title": post_title,
            "post_description": post_description,
        }
        return await self._send_request(HTTPMethod.POST, url, data)

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
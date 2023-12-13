import json
import logging
import os
import sys
from http import HTTPMethod, HTTPStatus

import aiohttp
from aiohttp import web, web_request
from aiohttp.web_exceptions import HTTPException

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Server:

    def __init__(self):
        self._name = self.__class__.__name__
        self._host = os.getenv("SERVER_HOST", "0.0.0.0")
        self._port = os.getenv("SERVER_PORT", 8000)
        self._chat_gpt_api_url = os.environ["CHAT_GPT_API_URL"]
        self._chat_gpt_api_key = os.environ["CHAT_GPT_API_KEY"]
        self._content_type = 'application/json'

        self._app = web.Application()
        self._app.router.add_route(
            method=HTTPMethod.GET,
            path="/ask_chat_gpt",
            handler=self.ask_chat_gpt,
        )

    def start(self):
        print(f"Starting the <{self._name}> at {self._host}:{self._port}")
        web.run_app(self._app, port=self._port)

    async def ask_chat_gpt(self, request: web_request.Request) -> web.Response:
        request_data = await request.json()
        if not (questions := request_data.get("questions")):
            return web.Response(
                status=HTTPStatus.BAD_REQUEST,
                text="no 'questions' parameter found in request"
            )

        if not isinstance(questions, (list, tuple)):
            return web.Response(
                status=HTTPStatus.BAD_REQUEST,
                text=f"'questions' parameter has invalid type: {type(questions)}"
            )

        answers = await self._request_chat_gpt(questions=questions)

        return web.Response(status=HTTPStatus.OK, text=json.dumps(answers))

    async def _request_chat_gpt(self, questions: list[str] | tuple[str, ...]) -> dict[str, str] | None:
        params = {"api_key": self._chat_gpt_api_key, "questions": questions}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._chat_gpt_api_url, params=params) as resp:
                    try:
                        return await resp.json()
                    except ValueError as exc:
                        logger.error(f"Cannot deserialize ChatGPT response: {str(exc)}")
                        return None
        except HTTPException as exc:
            logger.error(f"Communication with ChatGPT API was failed cause of: {str(exc)}")




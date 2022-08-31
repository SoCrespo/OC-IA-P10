
from dotenv import dotenv_values
from types import SimpleNamespace
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from http import HTTPStatus


config = SimpleNamespace(**dotenv_values())

async def messages(req: Request) -> Response:
    """
    Main bot message handler.
    """
    if "application/json" in req.headers["Content-Type"]:
        # response = await req.json()
        return Response(text="OK!", status=HTTPStatus.OK)
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)



async def health(req: Request) -> Response:
    """
    Check endpoint health.
    """
    return web.Response(text="App is running")

chatbot = web.Application()
chatbot.router.add_post("/api/messages", messages)
chatbot.router.add_get("/api/messages", health)

if __name__ == "__main__":
    web.run_app(chatbot, port=config.bot_port)

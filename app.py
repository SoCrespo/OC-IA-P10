import sys
print('**********************')
print('Starting app.py')
print('sys.path[0] is:')
print(sys.path[0])
print('**********************')
from dotenv import load_dotenv
import os
from types import SimpleNamespace
from aiohttp import web
from http import HTTPStatus
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter
from bot.flight_bot import FlightBot

load_dotenv()
config = SimpleNamespace(**os.environ)
settings= BotFrameworkAdapterSettings(config.bot_app_id, config.bot_app_password)
adapter = BotFrameworkAdapter(settings)
bot = FlightBot()

async def messages(req: web.Request) -> web.Response:
    """
    Main bot message handler.
    """
    if "application/json" not in req.headers["Content-Type"]:
        return web.Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    body = await req.json()
    activity = Activity().deserialize(body)

    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=HTTPStatus.OK)


async def health(req: web.Request) -> web.Response:
    """
    Check endpoint health.
    """
    return web.Response(text="App is running")

def init_func(argv):
    app = web.Application()
    app.router.add_post("", messages)
    app.router.add_get("", health)
    return app

if __name__ == "__main__":
    chatbot = init_func(None)
    web.run_app(chatbot, port=config.PORT)

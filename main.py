import asyncio
import logging
import sys
from typing import Any, Awaitable, Callable, Dict
from dotenv import dotenv_values
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiohttp import web

# Request
from aiohttp.web_request import Request

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import setup_application

from core.bridge import Bridge

config = dotenv_values(".env")

if not config["BOT_TOKEN"] or not config["WEBHOOK_SECRET"]:
    print("No BOT_TOKEN or WEBHOOK_SECRET variable found, bye")
    exit()

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8911
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = config["WEBHOOK_SECRET"]
BASE_WEBHOOK_URL = "https://damnbot.codedune.app"


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET
    )


dp = Dispatcher()
bridge = Bridge()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.reply("Damn...")


async def handle_webhook(request: Request):
    bot = request.app["bot"]
    dp = request.app["dp"]
    data = await request.json()
    if bridge.send_rpc("App.ProcessUpdates", data):
        await dp.feed_raw_update(bot, data)
    return web.Response(text="ok")


def main():
    dp.startup.register(on_startup)
    bot = Bot(
        config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    app = web.Application()
    app["bot"] = bot
    app["dp"] = dp

    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()

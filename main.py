import logging
import sys
from core.bridge import Bridge

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import web
from aiohttp.web_request import Request
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from getenv import getenv


BOT_TOKEN=getenv("BOT_TOKEN") or ""
WEBHOOK_URL=getenv("WEBHOOK_URL") or ""
WEBHOOK_SECRET=getenv("WEBHOOK_SECRET") or "damn"
WEBHOOK_PATH=getenv("WEBHOOK_PATH") or "/"
WEB_SERVER_HOST=getenv("WEB_SERVER_HOST") or "127.0.0.1"
WEB_SERVER_PORT=getenv("WEB_SERVER_PORT") or 8911


if not BOT_TOKEN or not WEBHOOK_URL:
    print("No BOT_TOKEN or WEBHOOK_URL variable found, bye")
    exit()


dp = Dispatcher()
bridge = Bridge()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.reply("Damn...")


async def handle_webhook(request: Request):
    bot = request.app["bot"]
    dp = request.app["dp"]

    data = await request.text()
    json = await request.json()
    
    if bridge.send_rpc("App.ProcessUpdates", data):
        await dp.feed_raw_update(bot, json)
    return web.Response(text="ok")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        WEBHOOK_URL+WEBHOOK_PATH, secret_token=WEBHOOK_SECRET
    )


def main():
    dp.startup.register(on_startup)
    bot = Bot(
        BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    app = web.Application()
    app["bot"] = bot
    app["dp"] = dp

    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=int(WEB_SERVER_PORT))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    main()

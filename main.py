import asyncio
from typing import Any, Awaitable, Callable, Dict
from dotenv import dotenv_values
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.bridge import Bridge

config = dotenv_values(".env")

if not config["BOT_TOKEN"]:
    print("No BOT_TOKEN variable found, bye")
    exit()

bot = Bot(config["BOT_TOKEN"])
dp = Dispatcher()


class GoMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.bridge = Bridge()
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore
        data: Dict[str, Any],
    ) -> Any:
        if self.bridge.send_rpc("App.ProcessUpdates", event.model_dump_json()):
            print("processing...")
            return await handler(event, data)
        print("Skipped update due to Goland said no")


dp.message.middleware(GoMiddleware())


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.reply("Damn...")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

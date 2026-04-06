from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
import asyncio

from config import BOT_TOKEN
from handlers import start, handle_buttons

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start, commands=["start"])
dp.callback_query.register(handle_buttons)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

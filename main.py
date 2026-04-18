from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio

from config import BOT_TOKEN
from handlers import start, handle_buttons

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start, Command("start"))

# باقي الرسائل
dp.message.register(lambda msg: handle_buttons(msg, bot))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

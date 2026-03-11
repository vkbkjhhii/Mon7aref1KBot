import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from handlers import register_handlers

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEV_ID = 7771042305  # حط هنا ID المطور

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# سجل كل handlers
register_handlers(dp, DEV_ID)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

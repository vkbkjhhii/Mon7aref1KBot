from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# تسجيل جميع الهاندلرز
register_handlers(dp)

# تشغيل البوت
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

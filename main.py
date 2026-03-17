import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from handlers import register_handlers

# التوكن من البيئة (يمكنك وضعه مباشرة بدل os.getenv إذا أحببت)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # أو ضع "توكن البوت هنا"
DEV_ID = 7771042305  # رقم حساب المطور

# إنشاء كائن البوت و Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# سجل كل handlers
register_handlers(dp, DEV_ID)

# تشغيل البوت
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

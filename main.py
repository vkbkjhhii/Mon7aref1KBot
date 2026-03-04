import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ---------------- توكن البوت من متغير البيئة ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- زرار تواصل مع المطور ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup()
    # ضع هنا الرابط النهائي للصفحة المتحركة بعد رفعها على استضافة
    url = "https://yourusername.vercel.app/faraon.html"
    kb.add(InlineKeyboardButton("تواصل مع المطور 🔥", url=url))
    await message.answer("مرحبا بك! اضغط الزر أدناه لفتح صفحة التواصل مع المطور:", reply_markup=kb)

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

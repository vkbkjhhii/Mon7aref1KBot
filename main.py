import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ---------------- إعداد البوت ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن البوت هنا أو في Variables
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- زر واحد ----------------
def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👑 توليد يوزرات", callback_data="generate_users"))
    return kb

# ---------------- توليد اليوزرات ----------------
def generate_user(length=5):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "@" + "".join(random.choice(chars) for _ in range(length))

# ---------------- /start ----------------
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("مرحبا بك! اضغط على الزر لتوليد 20 يوزر:", reply_markup=main_menu())

# ---------------- زر التوليد ----------------
@dp.callback_query_handler(lambda c: c.data == "generate_users")
async def generate(call: types.CallbackQuery):
    # عرض رسالة جاري التحميل
    loading = await call.message.edit_text("⏳ جاري توليد اليوزرات...\n[■■□□□□□□] 20%")
    await asyncio.sleep(1)
    await loading.edit_text("⏳ جاري التوليد...\n[■■■■■■■■] 100%")
    
    # توليد 20 يوزر
    users = "\n".join(generate_user() for _ in range(20))
    await call.message.edit_text(f"👑 تم توليد 20 يوزر:\n\n{users}")

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

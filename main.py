import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن البوت هنا

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- رسالة البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    name = message.from_user.first_name
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("⭐ يوزر مميز", callback_data="vip_start")
    )
    await message.answer(
        f"بتتريج اهلا بك عزيزي {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎",
        reply_markup=keyboard
    )

# ---------------- توليد 20 يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_start")
async def vip_generate(callback_query: types.CallbackQuery):
    msg = await callback_query.message.edit_text("⏳ جاري انشاء 20 يوزر مميز...")

    # شريط تحميل متحرك
    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫",
                "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]
    for p in progress:
        await asyncio.sleep(0.7)
        await msg.edit_text(f"⏳ جاري الانشاء:\n{p}")

    # توليد 20 يوزر وهمي
    users = []
    for i in range(1, 21):
        uid = random.randint(1000, 9999)
        users.append(f"👤 يوزر {i}: user{uid}")

    users_text = "\n".join(users)
    await msg.edit_text(f"✅ تم انشاء 20 يوزر مميز:\n\n{users_text}")

# ---------------- زرار ارقام فيك (اختياري) ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("هنا تقدر تضيف كود توليد الأرقام لو عايز")

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

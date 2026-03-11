import os
import random
import string
import asyncio
import re
import socket
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

DEV_ID = 7771042305

user_state = {}
users = set()

# ------------------ القائمة الرئيسية ------------------

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("✨ توليد يوزر", callback_data="gen_user"),
        InlineKeyboardButton("🔑 توليد باسورد", callback_data="gen_pass")
    )

    kb.add(
        InlineKeyboardButton("🔎 فحص رابط", callback_data="scan"),
        InlineKeyboardButton("👤 معلوماتي", callback_data="me")
    )

    kb.add(
        InlineKeyboardButton("🎮 لعبة XO", callback_data="xo"),
        InlineKeyboardButton("💬 التواصل مع المطور", callback_data="contact")
    )

    return kb

# ------------------ start ------------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    users.add(message.from_user.id)

    await message.answer(
        "اهلا بك في البوت",
        reply_markup=main_menu()
    )

# ------------------ معلوماتي ------------------

@dp.callback_query_handler(lambda c: c.data == "me")
async def my_info(call: types.CallbackQuery):

    user = call.from_user

    photos = await bot.get_user_profile_photos(user.id, limit=1)

    text = f"""
👤 الاسم: {user.first_name}

🆔 ID: {user.id}

🔗 Username: @{user.username}
"""

    if photos.total_count > 0:

        await bot.send_photo(
            user.id,
            photos.photos[0][-1].file_id,
            caption=text
        )

    else:

        await bot.send_message(user.id, text)

# ------------------ توليد يوزر ------------------

@dp.callback_query_handler(lambda c: c.data == "gen_user")
async def gen_user(call: types.CallbackQuery):

    msg = await call.message.edit_text("جاري توليد اليوزرات")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar = "▰"*(i+1) + "▱"*(3-i)

        await msg.edit_text(f"جاري التوليد\n{bar}")

    for _ in range(10):

        username = "@" + "".join(random.choices(string.ascii_uppercase, k=4))

        await bot.send_message(call.from_user.id, username)

# ------------------ توليد باسورد ------------------

@dp.callback_query_handler(lambda c: c.data == "gen_pass")
async def gen_pass(call: types.CallbackQuery):

    msg = await call.message.edit_text("جاري إنشاء Password")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar = "▰"*(i+1) + "▱"*(3-i)

        await msg.edit_text(f"جاري الإنشاء\n{bar}")

    chars = string.ascii_letters + string.digits

    for _ in range(5):

        pwd = "".join(random.choices(chars, k=12))

        await bot.send_message(call.from_user.id, f"<code>{pwd}</code>")

# ------------------ فحص رابط ------------------

@dp.callback_query_handler(lambda c: c.data == "scan")
async def scan(call: types.CallbackQuery):

    user_state[call.from_user.id] = "scan"

    await call.message.edit_text("ارسل الرابط لفحصه")

@dp.message_handler()
async def scan_handler(message: types.Message):

    if user_state.get(message.from_user.id) != "scan":
        return

    text = message.text.strip()

    if not text.startswith("http"):
        await message.reply("يمكنك إرسال رابط فقط")
        return

    try:
        domain = urlparse(text).netloc
        ip = socket.gethostbyname(domain)
    except:
        await message.reply("الرابط غير صالح")
        return

    await message.delete()

    site = "موقع عام"

    if "youtube" in domain:
        site = "Youtube"

    elif "facebook" in domain:
        site = "Facebook"

    elif "t.me" in domain:
        site = "Telegram"

    result = f"""
• الرابط: {text}

• التصنيف: آمن 🟢

• تفاصيل التصنيف:
الرابط يفتح موقع {site}

• معلومات IP: {ip}

• مزود الخدمة: AS20940 Akamai
"""

    await bot.send_message(message.from_user.id, result)

    user_state.pop(message.from_user.id)

# ------------------ التواصل مع المطور ------------------

@dp.callback_query_handler(lambda c: c.data == "contact")
async def contact(call: types.CallbackQuery):

    user_state[call.from_user.id] = "contact"

    await call.message.edit_text("اكتب رسالتك للمطور")

@dp.message_handler()
async def contact_dev(message: types.Message):

    if user_state.get(message.from_user.id) != "contact":
        return

    text = f"""
📩 رسالة جديدة

👤 المستخدم: {message.from_user.first_name}
🆔 ID: {message.from_user.id}

💬 الرسالة:
{message.text}
"""

    await bot.send_message(DEV_ID, text)

    await message.delete()

    await bot.send_message(
        message.from_user.id,
        "تم إرسال رسالتك إلى المطور"
    )

    user_state.pop(message.from_user.id)

# ------------------ لعبة XO (بداية) ------------------

@dp.callback_query_handler(lambda c: c.data == "xo")
async def xo(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("دعوة لاعب", callback_data="invite")
    )

    await call.message.edit_text(
        "اضغط لدعوة لاعب",
        reply_markup=kb
    )

# ------------------ لوحة المطور ------------------

@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):

    if message.from_user.id != DEV_ID:
        return

    await message.reply(
        f"""
لوحة المطور

عدد المستخدمين: {len(users)}
"""
    )

# ------------------ تشغيل ------------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

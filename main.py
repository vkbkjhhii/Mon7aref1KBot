import os
import random
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

user_state = {}

# ---------------- الدول ----------------
countries = {
    "egypt": ("🇪🇬 مصر", "+20"),
    "usa": ("🇺🇸 امريكا", "+1"),
    "uk": ("🇬🇧 بريطانيا", "+44"),
    "saudi": ("🇸🇦 السعودية", "+966"),
    "uae": ("🇦🇪 الامارات", "+971"),
    "morocco": ("🇲🇦 المغرب", "+212"),
    "algeria": ("🇩🇿 الجزائر", "+213"),
    "tunisia": ("🇹🇳 تونس", "+216"),
    "turkey": ("🇹🇷 تركيا", "+90"),
}

# ---------------- القائمة الرئيسية الاحترافية ----------------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("📱 ارقام فيك", callback_data="numbers"),
        InlineKeyboardButton("✨ صيد يوزر", callback_data="vip")
    )

    kb.add(
        InlineKeyboardButton("🔗 فحص الروابط", callback_data="check_link"),
        InlineKeyboardButton("🌟 شات المطور", callback_data="contact_dev")
    )

    kb.add(
        InlineKeyboardButton("🎮 لعبة X O", callback_data="xo_game"),
        InlineKeyboardButton("💳 توليد فيزا", callback_data="gen_visa")
    )

    kb.add(
        InlineKeyboardButton("📧 ايميل فيك", callback_data="fake_email"),
        InlineKeyboardButton("👤 معلومات حسابي", callback_data="my_info")
    )

    kb.add(
        InlineKeyboardButton("🌐 توليد IP", callback_data="gen_ip"),
        InlineKeyboardButton("🔑 باسورد قوي", callback_data="gen_pass")
    )

    kb.add(
        InlineKeyboardButton("☠️ انيميشن هاكر", callback_data="hacker_anim")
    )

    return kb


def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="home"))
    return kb

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("تم تسجيل الدخول بنجاح ☠️", reply_markup=main_menu())


@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    await callback.message.edit_text("القائمة الرئيسية", reply_markup=main_menu())


# ---------------- توليد فيزا ----------------
def generate_card():
    card = "4" + "".join(str(random.randint(0,9)) for _ in range(15))
    month = str(random.randint(1,12)).zfill(2)
    year = str(random.randint(2026,2032))
    cvv = str(random.randint(100,999))
    return card, month, year, cvv


@dp.callback_query_handler(lambda c: c.data == "gen_visa")
async def gen_visa(callback: types.CallbackQuery):

    msg = await callback.message.edit_text("جاري الاتصال بالبنوك...")

    anim = ["▒▒▒▒","█▒▒▒","██▒▒","███▒","████"]
    for a in anim:
        await asyncio.sleep(0.4)
        await msg.edit_text(f"جاري التوليد...\n{a}")

    card, m, y, cvv = generate_card()

    text = f"""
𝗣𝗮𝘀𝘀𝗲𝗱 ✅

Card : <code>{card}</code>
Expiry : {m}/{y}
CVV : {cvv}
"""

    await msg.edit_text(text, reply_markup=back_btn())


# ---------------- ايميل فيك ----------------
def generate_email():
    names = ["alex","dark","neo","ghost","alpha"]
    domains = ["gmail.com","outlook.com","yahoo.com"]
    return random.choice(names)+str(random.randint(100,9999))+"@"+random.choice(domains)


@dp.callback_query_handler(lambda c: c.data == "fake_email")
async def fake_email(callback: types.CallbackQuery):

    email = generate_email()

    text = f"""
📧 ايميل عشوائي

<code>{email}</code>
"""

    await callback.message.edit_text(text, reply_markup=back_btn())


# ---------------- معلومات المستخدم ----------------
@dp.callback_query_handler(lambda c: c.data == "my_info")
async def my_info(callback: types.CallbackQuery):

    user = callback.from_user

    text = f"""
👤 معلوماتك

ID : <code>{user.id}</code>
الاسم : {user.first_name}
اليوزر : @{user.username if user.username else "لا يوجد"}
"""

    await callback.message.edit_text(text, reply_markup=back_btn())


# ---------------- توليد IP ----------------
def generate_ip():
    return ".".join(str(random.randint(1,255)) for _ in range(4))


@dp.callback_query_handler(lambda c: c.data == "gen_ip")
async def gen_ip(callback: types.CallbackQuery):

    ip = generate_ip()

    text = f"""
🌐 IP عشوائي

<code>{ip}</code>
"""

    await callback.message.edit_text(text, reply_markup=back_btn())


# ---------------- باسورد قوي ----------------
def generate_password():
    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(16))


@dp.callback_query_handler(lambda c: c.data == "gen_pass")
async def gen_pass(callback: types.CallbackQuery):

    password = generate_password()

    text = f"""
🔑 باسورد قوي

<code>{password}</code>
"""

    await callback.message.edit_text(text, reply_markup=back_btn())


# ---------------- انيميشن ----------------
@dp.callback_query_handler(lambda c: c.data == "hacker_anim")
async def hacker_anim(callback: types.CallbackQuery):

    msg = await callback.message.edit_text("⚠️ بدء العملية...")

    frames=[
        "▒▒▒▒▒▒▒▒",
        "█▒▒▒▒▒▒▒",
        "██▒▒▒▒▒▒",
        "███▒▒▒▒▒",
        "████▒▒▒▒",
        "█████▒▒▒",
        "██████▒▒",
        "███████▒",
        "████████"
    ]

    for f in frames:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"Processing...\n{f}")

    await msg.edit_text("تمت العملية بنجاح ✔️", reply_markup=back_btn())


# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

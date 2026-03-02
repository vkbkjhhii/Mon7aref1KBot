import os
import random
import asyncio
import datetime
import string
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = "@x_1fn"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- التحقق من الاشتراك ----------------
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

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
    "germany": ("🇩🇪 ألمانيا", "+49"),
    "france": ("🇫🇷 فرنسا", "+33"),
    "italy": ("🇮🇹 ايطاليا", "+39"),
    "spain": ("🇪🇸 اسبانيا", "+34"),
    "canada": ("🇨🇦 كندا", "+1"),
    "brazil": ("🇧🇷 البرازيل", "+55"),
    "india": ("🇮🇳 الهند", "+91"),
    "russia": ("🇷🇺 روسيا", "+7"),
    "china": ("🇨🇳 الصين", "+86"),
    "japan": ("🇯🇵 اليابان", "+81"),
    "australia": ("🇦🇺 استراليا", "+61"),
}

# ---------------- توليد رقم ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

# ---------------- توليد يوزرات مميزة ----------------
def generate_vip_username():
    prefixes = ["S", "X", "I", "W", "F"]
    mid = random.choice(prefixes)
    nums = str(random.randint(10,99))
    suffix = random.choice(prefixes)
    return f"@{mid}_{nums}{suffix}"

# ---------------- القوائم ----------------
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("يوزر مميز 👑", callback_data="vip_user"),
        InlineKeyboardButton("معلومات حسابك 📋", callback_data="my_info"),
        InlineKeyboardButton("بوت اخر 🔗", url="https://t.me/ALMNHRF_Toobot?start=dd4c7ab7e035896f4bc454e9594d3b03992113")
    )
    return keyboard

back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home"))

# ---------------- /start ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("اشترك في القناة 📢", url=f"https://t.me/x_1fn")
        )
        return await message.answer("⚠️ لازم تشترك في القناة الأول", reply_markup=keyboard)

    name = message.from_user.first_name
    await message.answer(
        f"اهلا بك {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎",
        reply_markup=main_menu()
    )

# ---------------- رجوع للقائمة ----------------
@dp.callback_query_handler(lambda c: c.data == "back_home")
async def back_home(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("القائمة الرئيسية 🔥", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def choose_country(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in countries.items():
        keyboard.insert(InlineKeyboardButton(value[0], callback_data=f"country_{key}"))
    keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home"))
    await callback_query.message.edit_text("🌍 اختر الدولة", reply_markup=keyboard)

# ---------------- توليد الرقم ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]

    msg = await callback_query.message.edit_text("🔹 جاري انشاء الرقم...")

    progress = ["🟩⬜⬜⬜⬜", "🟩🟩⬜⬜⬜", "🟩🟩🟩⬜⬜", "🟩🟩🟩🟩⬜", "🟩🟩🟩🟩🟩"]
    for p in progress:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ جاري الانشاء...\n{p}")

    number = generate_number(country_code)
    tz = pytz.timezone("Africa/Cairo")
    now = datetime.datetime.now(tz)

    text = f"""
➖ رقم الهاتف ☎️ : <code>{number}</code>
➖ الدولة : {country_name}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M:%S')}
"""
    await msg.edit_text(text, reply_markup=back_keyboard)

# ---------------- يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_user")
async def vip_user(callback_query: types.CallbackQuery):
    msg = await callback_query.message.edit_text("🔄 جاري توليد 20 يوزر مميز...")

    progress = ["🟦⬜⬜⬜⬜⬜", "🟦🟦⬜⬜⬜⬜", "🟦🟦🟦⬜⬜⬜", "🟦🟦🟦🟦⬜⬜",
                "🟦🟦🟦🟦🟦⬜", "🟦🟦🟦🟦🟦🟦", "🟦🟦🟦🟦🟦🟦🟦"]
    for p in progress:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"👑 تجهيز اليوزرات...\n{p}")

    for _ in range(20):
        vip = generate_vip_username()
        await callback_query.message.answer(f"✅ : {vip}", reply_markup=back_keyboard)
        await asyncio.sleep(0.1)

# ---------------- معلومات حسابك ----------------
@dp.callback_query_handler(lambda c: c.data == "my_info")
async def my_info(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    tz = pytz.timezone("Africa/Cairo")
    now = datetime.datetime.now(tz)

    text = f"""
👤 الاسم: {user.first_name}
📎 اليوزر: @{user.username if user.username else "لا يوجد"}
🆔 الايدي: {user.id}
📅 التاريخ: {now.strftime('%Y-%m-%d')}
⏰ الوقت: {now.strftime('%H:%M:%S')}
"""

    msg = await callback_query.message.edit_text("")
    typed = ""
    for char in text:
        typed += char
        await msg.edit_text(typed)
        await asyncio.sleep(0.03)
    await msg.edit_reply_markup(reply_markup=back_keyboard)

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

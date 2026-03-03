import os
import random
import asyncio
import datetime
import pytz
import aiohttp
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

user_state = {}

# ---------------- الدول ----------------
countries = {
    "egypt": ("🇪🇬 مصر", "+20", "Africa/Cairo"),
    "usa": ("🇺🇸 امريكا", "+1", "America/New_York"),
    "uk": ("🇬🇧 بريطانيا", "+44", "Europe/London"),
    "saudi": ("🇸🇦 السعودية", "+966", "Asia/Riyadh"),
    "uae": ("🇦🇪 الامارات", "+971", "Asia/Dubai"),
    "morocco": ("🇲🇦 المغرب", "+212", "Africa/Casablanca"),
    "algeria": ("🇩🇿 الجزائر", "+213", "Africa/Algiers"),
    "tunisia": ("🇹🇳 تونس", "+216", "Africa/Tunis"),
    "turkey": ("🇹🇷 تركيا", "+90", "Europe/Istanbul"),
    "germany": ("🇩🇪 ألمانيا", "+49", "Europe/Berlin"),
    "france": ("🇫🇷 فرنسا", "+33", "Europe/Paris"),
    "italy": ("🇮🇹 ايطاليا", "+39", "Europe/Rome"),
    "spain": ("🇪🇸 اسبانيا", "+34", "Europe/Madrid"),
    "canada": ("🇨🇦 كندا", "+1", "America/Toronto"),
    "brazil": ("🇧🇷 البرازيل", "+55", "America/Sao_Paulo"),
    "india": ("🇮🇳 الهند", "+91", "Asia/Kolkata"),
    "russia": ("🇷🇺 روسيا", "+7", "Europe/Moscow"),
    "china": ("🇨🇳 الصين", "+86", "Asia/Shanghai"),
    "japan": ("🇯🇵 اليابان", "+81", "Asia/Tokyo"),
    "australia": ("🇦🇺 استراليا", "+61", "Australia/Sydney"),
}

# ---------------- قوائم ----------------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )
    kb.add(
        InlineKeyboardButton("فحص الروابط 🔗", callback_data="check_link")
    )
    kb.add(
        InlineKeyboardButton("بوت الاختراق", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("شات المطور 🌟", callback_data="contact_dev")
    )
    kb.add(
        InlineKeyboardButton("لعبة X O 🎮", callback_data="xo_game")
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("تم تسجيل الدخول اللي سيرفر المنحرف بنجاح 🏴‍☠️", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    user_state.pop(callback.from_user.id, None)
    await callback.message.edit_text("تم تسجيل الدخول اللي سيرفر المنحرف بنجاح 🏴‍☠️", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

def get_time_for_country(tz_str):
    tz = pytz.timezone(tz_str)
    return datetime.datetime.now(tz)

@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in countries.items():
        kb.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code, tz_str = countries[key]

    msg = await callback.message.edit_text("جاري فتح السيرفر ☣️...")
    hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
    for p in hacker_bar*3:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"جاري اختراق شريحة ال SIM :\n{p}")

    number = generate_number(code)
    now = get_time_for_country(tz_str)

    text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}"),
        InlineKeyboardButton("💬 طلب كود", callback_data="get_code")
    )
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    await msg.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code, tz_str = countries[key]

    number = generate_number(code)
    now = get_time_for_country(tz_str)

    text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""
    kb = callback.message.reply_markup
    await callback.message.edit_text(text, reply_markup=kb)

# ---------------- فحص الروابط الفعلي بدون توقف الأزرار ----------------
@dp.callback_query_handler(lambda c: c.data == "check_link")
async def check_link(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "check_link"
    await callback.message.edit_text("الرجاء ارسال الرابط لفحصه 🔎", reply_markup=None)

async def check_real_link(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, timeout=5) as resp:
                domain = urlparse(link).netloc
                status = resp.status
                if "wa.me" in domain or "api.whatsapp.com" in domain:
                    site_type = "واتساب"
                elif "t.me" in domain:
                    site_type = "تيليجرام"
                elif "facebook.com" in domain:
                    site_type = "فيسبوك"
                else:
                    site_type = "عام HTTPS"
                return f"""
• الرابط: {link}
• نوع الموقع: {site_type}
• الدومين: {domain}
• حالة HTTP: {status}
"""
    except:
        return f"الرابط: {link}\nحالة الرابط: غير شغال أو غير معروف ❌"

@dp.message_handler(lambda message: user_state.get(message.from_user.id) == "check_link")
async def handle_links(message: types.Message):
    state = user_state.get(message.from_user.id)
    if state == "check_link":
        await message.answer("⏳ جاري الفحص... ▰▰▰▱▱")
        asyncio.create_task(process_link(message))

async def process_link(message):
    result = await check_real_link(message.text.strip())
    await message.answer(result, reply_markup=back_btn())
    user_state.pop(message.from_user.id)

# ---------------- باقي البوت يظل كما هو ----------------
# باقي الأزرار والوظائف مثل VIP ولعبة X O وكل حاجة تعمل بدون أي توقف

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

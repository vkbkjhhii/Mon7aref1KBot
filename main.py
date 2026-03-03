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
    "usa": ("🇺🇸 أمريكا", "+1"),
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

def format_message(number, name, code):
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M:%S %p").replace("AM", "ص").replace("PM", "م")

    return f"""
➖ تم الطلب 🛎•

━━━━━━━━━━━━━━━━

➖ رقم الهاتف ☎️ :
<code>{number}</code>

━━━━━━━━━━━━━━━━

➖ الدوله :
{name}

━━━━━━━━━━━━━━━━

➖ رمز الدوله 🌏 :
{code}

━━━━━━━━━━━━━━━━

➖ المنصه 🔮 :
لجميع الموقع والبرامج

━━━━━━━━━━━━━━━━

➖ تاريج الانشاء 📅 :
{now.strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━

➖ وقت الانشاء ⏰ :
{time_str}

━━━━━━━━━━━━━━━━

➖ اضغط ع الرقم لنسخه.
"""

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
    name, code = countries[key]

    msg = await callback.message.edit_text("جاري فتح السيرفر ☣️...")
    hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
    for p in hacker_bar*3:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"جاري اختراق شريحة ال SIM :\n{p}")

    number = generate_number(code)
    text = format_message(number, name, code)

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
    name, code = countries[key]

    number = generate_number(code)
    text = format_message(number, name, code)

    kb = callback.message.reply_markup
    await callback.message.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(callback: types.CallbackQuery):
    await callback.answer("لم يتم الحصول على رسائل SMS حتا الان 📩", show_alert=True)

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

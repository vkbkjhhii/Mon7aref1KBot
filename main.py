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

# ---------------- الدول ----------------

countries = {
    "eg": ("🇪🇬 مصر", "+20"),
    "sa": ("🇸🇦 السعودية", "+966"),
    "us": ("🇺🇸 أمريكا", "+1"),
    "uk": ("🇬🇧 بريطانيا", "+44"),
    "fr": ("🇫🇷 فرنسا", "+33"),
    "de": ("🇩🇪 ألمانيا", "+49"),
    "tr": ("🇹🇷 تركيا", "+90"),
    "it": ("🇮🇹 إيطاليا", "+39"),
    "es": ("🇪🇸 إسبانيا", "+34"),
    "br": ("🇧🇷 البرازيل", "+55"),
    "in": ("🇮🇳 الهند", "+91"),
    "cn": ("🇨🇳 الصين", "+86"),
    "jp": ("🇯🇵 اليابان", "+81"),
    "ru": ("🇷🇺 روسيا", "+7"),
    "ca": ("🇨🇦 كندا", "+1"),
    "au": ("🇦🇺 أستراليا", "+61"),
    "mx": ("🇲🇽 المكسيك", "+52"),
    "id": ("🇮🇩 إندونيسيا", "+62"),
    "za": ("🇿🇦 جنوب أفريقيا", "+27"),
    "ae": ("🇦🇪 الإمارات", "+971"),
}

# ---------------- توليد رقم ----------------

def generate_number(code):
    return code + "".join(str(random.randint(0, 9)) for _ in range(8))

# ---------------- القائمة الرئيسية ----------------

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("ارقام فيك 🌐", callback_data="fake"))
    return kb

# ---------------- قائمة الدول ----------------

def countries_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key, value in countries.items():
        buttons.append(
            InlineKeyboardButton(value[0], callback_data=f"country_{key}")
        )
    kb.add(*buttons)
    kb.add(InlineKeyboardButton("🏠 رجوع", callback_data="main"))
    return kb

# ---------------- أزرار الرقم ----------------

def number_buttons(country_key):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{country_key}")
    )
    kb.add(
        InlineKeyboardButton("📩 طلب كود", callback_data="get_code")
    )
    return kb

# ---------------- /start ----------------

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("مرحباً بك 👋", reply_markup=main_menu())

# ---------------- رجوع ----------------

@dp.callback_query_handler(lambda c: c.data == "main")
async def back(call: types.CallbackQuery):
    await call.message.edit_text("القائمة الرئيسية 👇", reply_markup=main_menu())

# ---------------- زرار ارقام فيك ----------------

@dp.callback_query_handler(lambda c: c.data == "fake")
async def fake(call: types.CallbackQuery):
    await call.message.edit_text("🌍 اختر الدولة:", reply_markup=countries_menu())

# ---------------- اختيار دولة ----------------

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def show_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    await call.message.edit_text("⏳ جاري تحميل الرقم...")
    await asyncio.sleep(2)

    number = generate_number(code)
    now = datetime.datetime.now()

    text = f"""
📍 الدولة: {name}
☎️ الرقم: <code>{number}</code>

📅 التاريخ: {now.strftime("%d-%m-%Y")}
⏰ الوقت: {now.strftime("%H:%M:%S")}
"""

    await call.message.edit_text(text, reply_markup=number_buttons(key))

# ---------------- تغيير الرقم ----------------

@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    number = generate_number(code)
    now = datetime.datetime.now()

    text = f"""
📍 الدولة: {name}
☎️ الرقم: <code>{number}</code>

📅 التاريخ: {now.strftime("%d-%m-%Y")}
⏰ الوقت: {now.strftime("%H:%M:%S")}
"""

    await call.message.edit_text(text, reply_markup=number_buttons(key))

# ---------------- طلب كود ----------------

@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(call: types.CallbackQuery):
    await call.answer("📭 لم يصل أي كود حتى الآن", show_alert=True)

# ---------------- تشغيل البوت ----------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

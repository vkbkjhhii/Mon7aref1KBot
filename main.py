import os
import random
import asyncio
import datetime
import json
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = "Mon7aref1KBot"
DEV_NAME = "MOHAMED ELSAYED MOHAMED"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

USERS_FILE = "users.json"

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

# ---------------- حفظ المستخدم ----------------
def save_user(user_id):
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# ---------------- توليد رقم ----------------
def generate_number(code):
    return code + "".join(str(random.randint(0, 9)) for _ in range(8))

# ---------------- توليد يوزرات ----------------
def generate_user(length):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "@" + "".join(random.choice(chars) for _ in range(length))

# ---------------- القوائم ----------------
def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🌐 ارقام فيك", callback_data="fake"),
        InlineKeyboardButton("👑 يوزر مميز", callback_data="vip"),
        InlineKeyboardButton("🔗 فحص رابط", callback_data="scan")
    )
    return kb

def countries_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(name, callback_data=f"country_{key}") for key, (name, _) in countries.items()]
    kb.add(*buttons)
    kb.add(InlineKeyboardButton("🏠 رجوع", callback_data="main"))
    return kb

def number_buttons(country_key):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{country_key}"),
        InlineKeyboardButton("📩 طلب كود", callback_data="get_code")
    )
    kb.add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main"))
    return kb

def vip_menu():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔥 ثلاثي", callback_data="tri"),
        InlineKeyboardButton("💎 رباعي", callback_data="quad")
    )
    kb.add(InlineKeyboardButton("🏠 رجوع", callback_data="main"))
    return kb

# ---------------- رسالة مزخرفة ----------------
def profile_message(user: types.User):
    now = datetime.datetime.now()
    return f"""
╭───〔 {BOT_NAME} 〕───╮
👤 الاسم: {user.full_name}
🆔 ID: <code>{user.id}</code>
📛 اليوزر: @{user.username if user.username else "لا يوجد"}
📅 التاريخ: {now.strftime("%d-%m-%Y")}
⏰ الوقت: {now.strftime("%H:%M:%S")}
👨‍💻 المطور: {DEV_NAME}
╰─────────────────╯
"""

# ---------------- /start ----------------
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    save_user(msg.from_user.id)
    await msg.answer("مرحباً بك 👋", reply_markup=main_menu())

# ---------------- /restart ----------------
@dp.message_handler(commands=["restart"])
async def restart(msg: types.Message):
    user = msg.from_user
    save_user(user.id)
    photos = await bot.get_user_profile_photos(user.id, limit=1)
    text = profile_message(user)
    if photos.total_count > 0:
        await bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=text, reply_markup=main_menu())
    else:
        await msg.answer(text, reply_markup=main_menu())

# ---------------- رجوع للقائمة الرئيسية ----------------
@dp.callback_query_handler(lambda c: c.data == "main")
async def back(call: types.CallbackQuery):
    await call.message.edit_text("القائمة الرئيسية 👇", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data == "fake")
async def fake(call: types.CallbackQuery):
    await call.message.edit_text("🌍 اختر الدولة:", reply_markup=countries_menu())

# ---------------- اختيار دولة مع شريط تحميل ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def show_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    loading_msg = await call.message.edit_text("⏳ جاري تحميل الرقم...\n[░░░░░░░░░░] 0%")
    for i in range(1, 11):
        await asyncio.sleep(0.2)
        bar = "█" * i + "░" * (10 - i)
        await loading_msg.edit_text(f"⏳ جاري تحميل الرقم...\n[{bar}] {i*10}%")

    number = generate_number(code)
    now = datetime.datetime.now()
    text = f"""
📍 الدولة: {name}
☎️ الرقم: <code>{number}</code>
📅 التاريخ: {now.strftime("%d-%m-%Y")}
⏰ الوقت: {now.strftime("%H:%M:%S")}
"""
    await loading_msg.edit_text(text, reply_markup=number_buttons(key))

# ---------------- تغيير الرقم ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    loading_msg = await call.message.edit_text("🔄 جاري تغيير الرقم...\n[░░░░░░░░░░] 0%")
    for i in range(1, 11):
        await asyncio.sleep(0.1)
        bar = "█" * i + "░" * (10 - i)
        await loading_msg.edit_text(f"🔄 جاري تغيير الرقم...\n[{bar}] {i*10}%")

    number = generate_number(code)
    now = datetime.datetime.now()
    text = f"""
📍 الدولة: {name}
☎️ الرقم: <code>{number}</code>
📅 التاريخ: {now.strftime("%d-%m-%Y")}
⏰ الوقت: {now.strftime("%H:%M:%S")}
"""
    await loading_msg.edit_text(text, reply_markup=number_buttons(key))

# ---------------- طلب كود ----------------
@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(call: types.CallbackQuery):
    await call.answer("📭 لم يصل أي كود حتى الآن", show_alert=True)

# ---------------- واجهة VIP ----------------
@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(call: types.CallbackQuery):
    await call.message.edit_text("👑 اختر نوع اليوزر:", reply_markup=vip_menu())

@dp.callback_query_handler(lambda c: c.data in ["tri", "quad"])
async def gen_user(call: types.CallbackQuery):
    length = 3 if call.data == "tri" else 4
    msg = await call.message.edit_text("⏳ جاري توليد يوزرات مميزة...\n[■■□□□□□□] 20%")
    await asyncio.sleep(1)
    await msg.edit_text("⏳ جاري التوليد...\n[■■■■■■■■] 100%")
    users = "\n".join(generate_user(length) for _ in range(10))
    await asyncio.sleep(1)
    await msg.edit_text(f"👑 اليوزرات المميزة:\n\n{users}", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main")))

# ---------------- فحص الروابط ----------------
@dp.callback_query_handler(lambda c: c.data == "scan")
async def scan(call: types.CallbackQuery):
    await call.message.edit_text("🔗 أرسل الرابط لفحصه:")

@dp.message_handler(lambda m: m.text and m.text.startswith("http"))
async def scan_result(msg: types.Message):
    parsed = urlparse(msg.text)
    text = f"""
🔎 نتيجة الفحص:
🌍 الدومين: {parsed.netloc}
🔐 البروتوكول: {parsed.scheme}
📂 المسار: {parsed.path}
"""
    await msg.answer(text, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main")))

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

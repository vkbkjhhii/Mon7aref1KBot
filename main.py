import os
import random
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = "@x_1fn"  # قناة الاشتراك الإجباري
BOT_NAME = "Mon7aref1KBot"
DEV_NAME = "MOHAMED ELSAYED MOHAMED"

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

# ---------------- التحقق من الاشتراك ----------------
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ---------------- توليد الرقم ----------------
def generate_number(code):
    return code + "".join(str(random.randint(0, 9)) for _ in range(8))

# ---------------- القوائم ----------------
def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🌐 أرقام فيك", callback_data="fake"))
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
        InlineKeyboardButton("🔁 تغيير الرقم", callback_data=f"change_{country_key}"),
        InlineKeyboardButton("📩 طلب كود", callback_data="get_code")
    )
    kb.add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main"))
    return kb

# ---------------- رسالة الترحيب مزخرفة ----------------
def profile_message(user: types.User):
    now = datetime.datetime.now()
    return f"""
╭───〔 {BOT_NAME} 〕───╮

👤 الاسم: {user.full_name}

📛 اليوزر: @{user.username if user.username else "لا يوجد"}

⏰ الوقت: {now.strftime("%H:%M:%S")}

📅 التاريخ: {now.strftime("%d-%m-%Y")}

╰─────────────────╯
"""

# ---------------- /start ----------------
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user = msg.from_user
    if not await check_sub(user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك الآن ✅", url=f"https://t.me/{FORCE_CHANNEL.replace('@','')}"))
        return await msg.answer("⚠️ يجب الاشتراك في القناة أولاً", reply_markup=kb)

    photos = await bot.get_user_profile_photos(user.id, limit=1)
    text = profile_message(user)
    if photos.total_count > 0:
        await bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=text, reply_markup=main_menu())
    else:
        await msg.answer(text, reply_markup=main_menu())

# ---------------- رجوع للقائمة الرئيسية ----------------
@dp.callback_query_handler(lambda c: c.data == "main")
async def back(call: types.CallbackQuery):
    user = call.from_user
    text = profile_message(user)
    await call.message.edit_text(text, reply_markup=main_menu())

# ---------------- أرقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data == "fake")
async def fake(call: types.CallbackQuery):
    await call.message.edit_text("🌍 اختر الدولة:", reply_markup=countries_menu())

# ---------------- اختيار دولة ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def show_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    loading_msg = await call.message.edit_text("⏳ جاري إنشاء الرقم...\n[░░░░░░░░░░] 0%")
    for i in range(1, 11):
        await asyncio.sleep(0.2)
        bar = "█" * i + "░" * (10 - i)
        await loading_msg.edit_text(f"⏳ جاري إنشاء الرقم...\n[{bar}] {i*10}%")

    number = generate_number(code)
    await loading_msg.edit_text(
        f"🎉 تم إنشاء الرقم!\n\n📍 الدولة: {name}\n☎️ الرقم: <code>{number}</code>\n⏰ الوقت: {datetime.datetime.now().strftime('%H:%M:%S')}\n📅 التاريخ: {datetime.datetime.now().strftime('%d-%m-%Y')}",
        reply_markup=number_buttons(key)
    )

# ---------------- تغيير الرقم ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change_number(call: types.CallbackQuery):
    key = call.data.split("_")[1]
    name, code = countries[key]

    loading_msg = await call.message.edit_text("🔁 جاري تغيير الرقم...\n[░░░░░░░░░░] 0%")
    for i in range(1, 11):
        await asyncio.sleep(0.1)
        bar = "█" * i + "░" * (10 - i)
        await loading_msg.edit_text(f"🔁 جاري تغيير الرقم...\n[{bar}] {i*10}%")

    number = generate_number(code)
    await loading_msg.edit_text(
        f"📍 الدولة: {name}\n☎️ الرقم: <code>{number}</code>\n⏰ الوقت: {datetime.datetime.now().strftime('%H:%M:%S')}\n📅 التاريخ: {datetime.datetime.now().strftime('%d-%m-%Y')}",
        reply_markup=number_buttons(key)
    )

# ---------------- طلب كود ----------------
@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(call: types.CallbackQuery):
    await call.answer("📭 لم يصل أي كود حتى الآن", show_alert=True)

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import os
import random
import asyncio
import datetime
import string
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@x_1fn"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

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

# ---------------- تحقق الاشتراك ----------------
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# ---------------- توليد رقم ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

# ---------------- توليد يوزر ----------------
def generate_username():
    letters = string.ascii_lowercase
    length = random.randint(6, 9)
    return ''.join(random.choice(letters) for _ in range(length))

# ---------------- الشاشة الرئيسية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("اشترك في القناة 🔔", url="https://t.me/x_1fn"))
        await message.answer("⚠️ يجب الاشتراك في القناة لاستخدام البوت", reply_markup=keyboard)
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"))
    keyboard.add(InlineKeyboardButton("⭐ يوزر مميز", callback_data="vip_user"))
    keyboard.add(InlineKeyboardButton("👤 معلوماتك كمستخدم", callback_data="my_info"))

    await message.answer("اهلا بك في بوت المنحرف 💎", reply_markup=keyboard)

# ---------------- ارقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def choose_country(callback_query: types.CallbackQuery):

    if not await check_subscription(callback_query.from_user.id):
        await callback_query.answer("اشترك في القناة أولا ❌", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in countries.items():
        keyboard.insert(
            InlineKeyboardButton(value[0], callback_data=f"country_{key}")
        )

    await callback_query.message.edit_text("🌍 اختر الدولة", reply_markup=keyboard)

# ---------------- توليد الرقم ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]

    msg = await callback_query.message.edit_text("⏳ جاري انشاء الرقم...")

    for i in range(6):
        await asyncio.sleep(0.4)
        await msg.edit_text(f"⏳ جاري الانشاء...\n{'🔹'* (i+1)}")

    number = generate_number(country_code)
    now = datetime.datetime.now()

    text = f"""
📱 رقم من سيرفر المنحرف

<code>{number}</code>

🌍 {country_name}
📅 {now.strftime('%Y-%m-%d')}
⏰ {now.strftime('%H:%M:%S')}
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}")
    )

    await msg.edit_text(text, reply_markup=keyboard)

# ---------------- يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_user")
async def vip_user(callback_query: types.CallbackQuery):

    msg = await callback_query.message.answer("⏳ جاري توليد 10 يوزرات مميزة...")

    for i in range(5):
        await asyncio.sleep(0.3)
        await msg.edit_text(f"⏳ جاري التوليد...\n{'🟢'* (i+1)}")

    usernames = "\n".join([f"<code>@{generate_username()}</code>" for _ in range(10)])

    await msg.edit_text(f"⭐ يوزرات مميزة:\n\n{usernames}")

# ---------------- معلومات المستخدم (حرف حرف) ----------------
@dp.callback_query_handler(lambda c: c.data == "my_info")
async def my_info(callback_query: types.CallbackQuery):

    user = callback_query.from_user
    now = datetime.datetime.now()

    text = f"""👤 معلوماتك كمستخدم

الاسم: {user.first_name}
اليوزر: @{user.username if user.username else "لا يوجد"}
ID: {user.id}
التاريخ: {now.strftime('%Y-%m-%d')}
الوقت: {now.strftime('%H:%M:%S')}
"""

    msg = await callback_query.message.answer("")

    displayed = ""
    for char in text:
        displayed += char
        await msg.edit_text(displayed)
        await asyncio.sleep(0.02)

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

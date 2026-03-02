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

# ---------------- ستارت ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    name = message.from_user.first_name
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"))
    
    await message.answer(
        f"بتتريج اهلا بك عزيزي {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎",
        reply_markup=keyboard
    )

# ---------------- اختيار الدولة ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def choose_country(callback_query: types.CallbackQuery):
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

    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫", 
                "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]

    for p in progress:
        await asyncio.sleep(0.7)
        await msg.edit_text(f"⏳ إنشاء الرقم:\n{p}")

    number = generate_number(country_code)
    now = datetime.datetime.now()

    text = f"""📱 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 - رقم من سيرفر المنحرف 📱

➖ تم انشاء الرقم 🛎

──────────────

➖ رقم الهاتف ☎️ : <code>{number}</code>

➖ الدولة 🌍 : {country_name}

➖ رمز الدولة 🌏 : {country_code}

──────────────

➖ المنصة 🔮 : لجميع المواقع والبرامج

──────────────

➖ تاريخ الانشاء 📅 : {now.strftime('%Y-%m-%d')}

➖ وقت الانشاء ⏰ : {now.strftime('%I:%M %p')}

──────────────

➖ اضغط على الرقم لنسخه.
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}")
    )
    keyboard.add(
        InlineKeyboardButton("💬 طلب الكود", callback_data="get_code")
    )
    keyboard.add(
        InlineKeyboardButton("⭐ يوزر مميز", callback_data="vip_user")
    )

    await msg.edit_text(text, reply_markup=keyboard)

# ---------------- طلب الكود ----------------
@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(callback_query: types.CallbackQuery):
    await callback_query.answer("لا توجد رسائل جديدة 📂", show_alert=True)

# ---------------- يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_user")
async def vip_user(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.first_name
    user_id = callback_query.from_user.id
    await callback_query.answer(
        f"⭐ يوزر مميز\n👤 الاسم: {user_name}\n🆔 ID: {user_id}\nمرحباً بك في سيرفر المنحرف",
        show_alert=True
    )

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

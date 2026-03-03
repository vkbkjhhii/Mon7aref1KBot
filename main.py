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
        InlineKeyboardButton("اختراق واتساب", callback_data="whatsapp_link"),
        InlineKeyboardButton("اختراق فيسبوك", callback_data="facebook_link")
    )
    kb.add(
        InlineKeyboardButton("بوت الاختراق 👾", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("شات المطور 🌟", callback_data="contact_dev")
    )
    kb.add(InlineKeyboardButton("لعبة X O 🎮", callback_data="xo_game"))

    # ----------- الزر الجديد فقط -----------
    kb.add(InlineKeyboardButton("💳 توليد كارت", callback_data="generate_card"))

    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ---------------- توليد كارت (إضافة جديدة فقط) ----------------
def generate_demo_card():
    names = ["Kali Herman V", "Alex Morgan", "David Stone", "Sara Wilson", "Michael Brown"]
    name = random.choice(names)
    card_number = "DEMO-" + str(random.randint(10000000, 99999999))
    month = random.randint(1, 12)
    year = random.randint(26, 32)
    cvv = random.randint(100, 999)
    pin = random.randint(1000, 9999)
    balance = random.randint(10, 100)

    return f"""
========== 💳 DEMO CARD ==========

🆔 رقم البطاقة: {card_number}
👤 اسم صاحب البطاقة: {name}
📅 تاريخ الانتهاء: {month:02d}/{year}
🔒 رمز (CVV): {cvv}
🔑 الرقم التجريبي (PIN): {pin}
💵 رصيد تجريبي: ${balance}

⚠️ بطاقة محاكاة غير حقيقية

========== 💳 DEMO CARD ==========
"""

@dp.callback_query_handler(lambda c: c.data == "generate_card")
async def generate_card_handler(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "⏳ جاري توليد الكارت...")
    await asyncio.sleep(2)
    card_text = generate_demo_card()
    await bot.send_message(callback.from_user.id, card_text, reply_markup=back_btn())

# ---------------- باقي كودك القديم بدون أي تغيير ----------------
# (من أول start لحد XO والـ polling زي ما هو بالظبط)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🏠 القائمة الرئيسية", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    user_state.pop(callback.from_user.id, None)
    await callback.message.edit_text("🏠 القائمة الرئيسية", reply_markup=main_menu())

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

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
        InlineKeyboardButton("فحص الروابط 🔗", callback_data="check_link"),
        InlineKeyboardButton("فيزا 💳", callback_data="visa")
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

# ---------------- فيزا ----------------
def generate_visa():
    number = "475055" + str(random.randint(1000000000,9999999999))[:10]
    exp_month = random.randint(1,12)
    exp_year = random.randint(2026,2030)
    cvv = random.randint(100,999)
    value = random.randint(10,100)
    return number, exp_month, exp_year, cvv, value

@dp.callback_query_handler(lambda c: c.data == "visa")
async def visa(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("جاري الاتصال بسيرفر البنوك 💳")

    anim = [
        "🟥🟧🟨🟩🟦🟪",
        "🟪🟦🟩🟨🟧🟥",
        "🟩🟨🟥🟦🟧🟪",
        "🟦🟥🟧🟩🟪🟨"
    ]

    for i in range(8):
        await asyncio.sleep(0.4)
        await msg.edit_text(f"جاري توليد بطاقة...\n{anim[i%4]}")

    number, m, y, cvv, value = generate_visa()

    text=f"""
𝗣𝗮𝘀𝘀𝗲𝗱 ✅
[-] Card Number : {number}
[-] Expiry : {m:02d}/{y}
[-] CVV : {cvv}
[-] Bank : U.S. Bank
[-] Card Type : VISA - DEBIT - VISA CLASSIC
[-] Country : USA🇺🇸
[-] Value : ${value}
============================
[-] by : BOT
"""

    kb=InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 توليد فيزا جديدة",callback_data="visa"),
        InlineKeyboardButton("🔙 العودة",callback_data="home")
    )

    await msg.edit_text(text,reply_markup=kb)

# ---------------- باقي الكود كما هو ----------------

# (كل الكود القديم بتاعك يفضل كما هو بدون أي تغيير)

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

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
DEV_ID = 7771042305

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

# ---------------- القائمة الرئيسية ----------------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )
    kb.add(InlineKeyboardButton("فحص الروابط 🔗", callback_data="check_link"))
    kb.add(
        InlineKeyboardButton("بوت الاختراق", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("شات المطور 🌟", callback_data="contact_dev")
    )
    kb.add(InlineKeyboardButton("لعبة X O 🎮", callback_data="xo_game"))
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ---------------- VIP المخفي (مدفوع) ----------------
vip_hidden_kb = InlineKeyboardMarkup(row_width=3)

buttons = [
    "زر 1","زر 2","زر 3",
    "زر 4","زر 5","زر 6",
    "زر 7","زر 8","زر 9"
]

for i, name in enumerate(buttons):
    vip_hidden_kb.insert(
        InlineKeyboardButton(name, callback_data=f"paid_{i}")
    )

vip_hidden_kb.add(
    InlineKeyboardButton("💰 شراء عملات البوت", url=f"https://t.me/{DEV_ID}")
)

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("تم تسجيل الدخول اللي سيرفر المنحرف بنجاح 🏴‍☠️", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    user_state.pop(callback.from_user.id, None)
    await callback.message.edit_text("تم تسجيل الدخول اللي سيرفر المنحرف بنجاح 🏴‍☠️", reply_markup=main_menu())

# ---------------- عرض VIP ----------------
@dp.message_handler(lambda message: message.text and message.text.lower() == "vip")
async def show_vip(message: types.Message):
    await message.answer("تم الدخول اللي السيرفر المدفوع 😈", reply_markup=vip_hidden_kb)

@dp.callback_query_handler(lambda c: c.data.startswith("paid_"))
async def paid_buttons(callback: types.CallbackQuery):
    await callback.answer(
        "🚫 هذا الخيار مدفوع\n"
        "💎 يجب شحن عملات البوت أولاً\n"
        "اضغط على شراء عملات البوت للتفعيل",
        show_alert=True
    )

# ---------------- تواصل مع المطور ----------------
@dp.callback_query_handler(lambda c: c.data == "contact_dev")
async def contact_dev(callback: types.CallbackQuery):
    await callback.message.answer(
        "💎 نظام شحن عملات البوت\n\n"
        "لشراء العملات يرجى التواصل مع المطور مباشرة ⏳",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("📩 تواصل مع المطور", url=f"https://t.me/f_zm1")
        )
    )

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

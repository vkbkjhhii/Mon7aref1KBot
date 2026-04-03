import os
import openai
from aiogram import types
from buttons import main_menu, back_btn, far3od_menu
import random, datetime, asyncio, pytz
from urllib.parse import urlparse

# ===================== ضع مفتاحك هنا =====================
openai.api_key = os.getenv("OPENAI_API_KEY")
# ==========================================================

user_state = {}
ai_sessions = {}  # تتبع جلسات الذكاء الاصطناعي

real_numbers = {
    "مصر":["01012345678","01198765432","01234567890"],
    "امريكا":["+12025550123","+12025550987","+12125551234"],
    "بريطانيا":["+447911123456","+447912345678","+447913456789"],
    "السعودية":["+966501234567","+966512345678","+966513456789"],
    "الامارات":["+971501234567","+971512345678","+971513456789"],
    "المغرب":["+212612345678","+212612345679","+212612345680"],
    "الجزائر":["+213550123456","+213550123457","+213550123458"],
    "تونس":["+21620123456","+21620123457","+21620123458"],
    "تركيا":["+905012345678","+905012345679","+905012345680"],
    "ألمانيا":["+4915123456789","+4915123456790","+4915123456791"],
    "فرنسا":["+33612345678","+33612345679","+33612345680"],
    "إيطاليا":["+393123456789","+393123456780","+393123456781"],
    "إسبانيا":["+34612345678","+34612345679","+34612345680"],
    "كندا":["+12041234567","+12041234568","+12041234569"],
    "البرازيل":["+5511998765432","+5511998765433","+5511998765434"],
    "الهند":["+919812345678","+919812345679","+919812345680"],
    "روسيا":["+79161234567","+79161234568","+79161234569"],
    "الصين":["+8613800138000","+8613800138001","+8613800138002"],
    "اليابان":["+819012345678","+819012345679","+819012345680"],
    "استراليا":["+61412345678","+61412345679","+61412345680"]
}

CHANNEL_1 = "@fraon10k"
CHANNEL_2 = "@feraon_1"

async def is_subscribed(bot, user_id):
    try:
        member1 = await bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await bot.get_chat_member(CHANNEL_2, user_id)
        return member1.status != "left" and member2.status != "left"
    except:
        return False

def register_handlers(dp, DEV_ID):
    tz = pytz.timezone("Africa/Cairo")

    # ---------- START ----------
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        if await is_subscribed(dp.bot, message.from_user.id):
            await message.answer(f"اهلا بك {message.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())
        else:
            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton("اشترك ▪️", url="https://t.me/fraon10k"),
                types.InlineKeyboardButton("اشترك ▪️", url="https://t.me/feraon_1")
            )
            kb.add(types.InlineKeyboardButton("✅ تحقق", callback_data="check_sub"))
            await message.answer("الرجاء الاشتراك في جميع قنوات المطور قبل استخدام البوت.", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data=="check_sub")
    async def check_sub(callback: types.CallbackQuery):
        if await is_subscribed(dp.bot, callback.from_user.id):
            await callback.message.edit_text(f"اهلا بك {callback.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())
        else:
            await callback.answer("لم تشترك بعد في القنوات", show_alert=True)

    @dp.callback_query_handler(lambda c: c.data=="home")
    async def home(callback: types.CallbackQuery):
        user_state.pop(callback.from_user.id, None)
        ai_sessions.pop(callback.from_user.id, None)
        await callback.message.edit_text(f"اهلا بك {callback.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())

    # ====================== زرار الذكاء الاصطناعي ======================
    @dp.callback_query_handler(lambda c: c.data == "ai_mode")
    async def ai_mode_handler(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        ai_sessions[user_id] = True
        msg = await callback.message.answer(
            "🤖 بدأت المحادثة مع

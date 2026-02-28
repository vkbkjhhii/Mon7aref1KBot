import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================== الإعدادات ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = "@x_1fn"
DEV_LINK = "https://t.me/f_zm1"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ================== زرار الاشتراك ==================
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================== /start ==================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    subscribed = await check_subscription(message.from_user.id)

    if not subscribed:
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{FORCE_CHANNEL.replace('@','')}")
        )
        kb.add(
            InlineKeyboardButton("تحقق من الاشتراك", callback_data="check_sub")
        )

        await message.answer("🚫 لازم تشترك في القناة الأول", reply_markup=kb)
        return

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📺 قنوات التليفزيون", callback_data="tv"),
        InlineKeyboardButton("🤖 ذكاء اصطناعي", callback_data="ai"),
        InlineKeyboardButton("👨‍💻 المطور", url=DEV_LINK)
    )

    await message.answer("🔥 أهلاً بيك في البوت الاحترافي", reply_markup=kb)

# ================== تحقق الاشتراك ==================
@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_sub(call: types.CallbackQuery):
    subscribed = await check_subscription(call.from_user.id)

    if subscribed:
        await call.message.delete()
        await start(call.message)
    else:
        await call.answer("لسه مشتركتش ❌", show_alert=True)

# ================== قنوات التليفزيون ==================
@dp.callback_query_handler(lambda c: c.data == "tv")
async def tv_channels(call: types.CallbackQuery):
    await call.message.answer(
        "🔗 https://5b622f07944df.streamlock.net/aghapy.tv/aghapy.smil/playlist.m3u8\n\n"
        "🔹 Al Ghad TV (1080p)\n"
        "🔗 https://eazyvw.com/alghad.m3u8"
    )

# ================== ذكاء اصطناعي بسيط ==================
user_waiting_ai = {}

@dp.callback_query_handler(lambda c: c.data == "ai")
async def ai_start(call: types.CallbackQuery):
    user_waiting_ai[call.from_user.id] = True
    await call.message.answer("🤖 ابعتلي سؤالك...")

@dp.message_handler()
async def ai_reply(message: types.Message):
    if user_waiting_ai.get(message.from_user.id):
        user_waiting_ai[message.from_user.id] = False
        await message.reply("🔥 ده رد تجريبي للذكاء الاصطناعي")

# ================== تشغيل البوت ==================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

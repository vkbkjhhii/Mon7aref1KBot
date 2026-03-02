import os
import random
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ضع توكن البوت هنا
CHANNEL = "@x_1fn"  # قناة الاشتراك الاجباري

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- توليد usernames ----------------
def generate_username(i):
    # ممكن تغير الصيغة حسب رغبتك
    names = ["Shadow", "Falcon", "Tiger", "Phoenix", "Dragon", "Wolf", "Eagle", "Lion", "Ninja", "Ghost"]
    return f"<code>{random.choice(names)}_{i}</code>"

# ---------------- فحص الاشتراك ----------------
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        if member.status in ["left", "kicked"]:
            return False
        return True
    except:
        return False

# ---------------- ستارت ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    subscribed = await check_subscription(user_id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn"))
        await message.answer("❌ يجب الاشتراك في القناة قبل استخدام البوت!", reply_markup=keyboard)
        return

    name = message.from_user.first_name
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("⭐ يوزر مميز", callback_data="vip_start"))
    await message.answer(f"بتتريج اهلا بك عزيزي {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎", reply_markup=keyboard)

# ---------------- توليد 20 يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_start")
async def vip_generate(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn"))
        await callback_query.message.edit_text("❌ يجب الاشتراك في القناة قبل استخدام البوت!", reply_markup=keyboard)
        return

    msg = await callback_query.message.edit_text("⏳ جاري انشاء 20 يوزر مميز...")

    # شريط تحميل متحرك
    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫", "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]
    for p in progress:
        await asyncio.sleep(0.7)
        await msg.edit_text(f"⏳ جاري الانشاء:\n{p}")

    # توليد 20 username حقيقي
    users = [generate_username(i) for i in range(1, 21)]
    users_text = "\n".join(users)

    # زرار معلومات المستخدم
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("ℹ️ معلوماتك كمستخدم", callback_data="user_info"))

    final_text = f"✅ تم انشاء 20 يوزر مميز ✨\n\n{users_text}\n\n🌟 استمتع باليوزرز المميزة 🌟"
    await msg.edit_text(final_text, reply_markup=keyboard)

# ---------------- زر معلومات المستخدم ----------------
@dp.callback_query_handler(lambda c: c.data == "user_info")
async def user_info(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    now = datetime.datetime.now()
    text = f"""ℹ️ معلوماتك كمستخدم:

➖ الاسم: {user.first_name}
➖ اليوزر تيك: @{user.username if user.username else 'لا يوجد'}
➖ التاريخ: {now.strftime('%Y-%m-%d')}
➖ الوقت: {now.strftime('%I:%M %p')}
"""
    await callback_query.answer(text, show_alert=True)

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

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

# ================== إعدادات ==================
DEV_ID = 7771042305
CHANNELS = ["@fraon10k", "@x_1fn"]
user_state = {}

# ================== تحقق الاشتراك ==================
async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

async def force_sub(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📢 القناة الأولى", url="https://t.me/fraon10k"),
        InlineKeyboardButton("📢 القناة الثانية", url="https://t.me/x_1fn"),
    )
    kb.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
    await message.answer("🚨 يجب الاشتراك في القنوات أولاً:", reply_markup=kb)

# ================== القائمة الرئيسية ==================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("يوزر مميز 👑", callback_data="vip")
    )
    kb.add(
        InlineKeyboardButton("بطاقات وهمية 💳", callback_data="fake_card"),
        InlineKeyboardButton("فحص الروابط 🔗", callback_data="check_link")
    )
    kb.add(
        InlineKeyboardButton("تغيير شكل رابط 🔄", callback_data="mask_link"),
        InlineKeyboardButton("تواصل مع المطور ☎️", callback_data="contact_dev")
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ================== البداية ==================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        await force_sub(message)
        return
    await message.answer("👋 أهلاً بك في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅↝ ①", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def recheck(callback: types.CallbackQuery):
    if await check_sub(callback.from_user.id):
        await callback.message.edit_text("✅ تم التحقق بنجاح!", reply_markup=main_menu())
    else:
        await callback.answer("❌ لم تشترك بعد", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    user_state.pop(callback.from_user.id, None)
    await callback.message.edit_text("🏠 القائمة الرئيسية", reply_markup=main_menu())

# ================== أرقام فيك ==================
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

countries = {
    "egypt": ("🇪🇬 مصر", "+20"),
    "usa": ("🇺🇸 امريكا", "+1"),
}

@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    for k, v in countries.items():
        kb.add(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    await callback.message.edit_text("🌍 اختر الدولة", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code = countries[key]
    number = generate_number(code)
    await callback.message.edit_text(
        f"📱 الرقم:\n<code>{number}</code>\n🌍 الدولة: {name}",
        reply_markup=back_btn()
    )

# ================== يوزر مميز ==================
def generate_user():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
    return "@" + "".join(random.choice(chars) for _ in range(4))

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    for _ in range(5):
        await callback.message.answer(generate_user())
        await asyncio.sleep(0.3)
    await callback.message.answer("✅ انتهى التوليد", reply_markup=back_btn())

# ================== بطاقات وهمية ==================
def generate_fake_card():
    number = "".join(str(random.randint(0, 9)) for _ in range(16))
    exp = f"{random.randint(1,12):02d}/{random.randint(24,30)}"
    cvv = random.randint(100, 999)
    return number, exp, cvv

@dp.callback_query_handler(lambda c: c.data == "fake_card")
async def fake_card(callback: types.CallbackQuery):
    number, exp, cvv = generate_fake_card()
    text = f"""
💳 بطاقة وهمية:

➖ الرقم: <code>{number}</code>
➖ الانتهاء: {exp}
➖ CVV: {cvv}
"""
    await callback.message.edit_text(text, reply_markup=back_btn())

# ================== فحص الروابط ==================
@dp.callback_query_handler(lambda c: c.data == "check_link")
async def check_link(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "check_link"
    await callback.message.edit_text("🔗 أرسل الرابط للفحص:")

# ================== تغيير شكل الرابط ==================
@dp.callback_query_handler(lambda c: c.data == "mask_link")
async def mask_link(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "mask_link"
    await callback.message.edit_text("🔄 أرسل الرابط لتغيير شكله:")

# ================== التواصل مع المطور ==================
@dp.callback_query_handler(lambda c: c.data == "contact_dev")
async def contact_dev(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "contact_dev"
    await callback.message.edit_text("📩 اكتب رسالتك لإرسالها للمطور:", reply_markup=back_btn())

# ================== معالجة الرسائل ==================
@dp.message_handler()
async def handle_messages(message: types.Message):
    state = user_state.get(message.from_user.id)

    if state == "check_link":
        await message.answer("✅ الرابط آمن (فحص تجريبي)", reply_markup=back_btn())
        user_state.pop(message.from_user.id)
        return

    if state == "mask_link":
        link = message.text.strip()
        if not link.startswith("http"):
            link = "https://" + link
        masked = link.replace("https://", "https://secure-")
        await message.answer(f"🔄 الشكل الجديد:\n{masked}", reply_markup=back_btn())
        user_state.pop(message.from_user.id)
        return

    if state == "contact_dev":
        if message.from_user.id != DEV_ID:
            await bot.send_message(
                DEV_ID,
                f"💬 رسالة من {message.from_user.first_name}\nID: {message.from_user.id}\n\n{message.text}"
            )
            await message.answer("✅ تم إرسال رسالتك")
        return

# ================== تشغيل ==================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

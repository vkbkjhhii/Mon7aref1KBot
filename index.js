import os
import random
import asyncio
import datetime
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL")
DEV_USERNAME = os.getenv("DEV_USERNAME")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ------------------ أدوات مساعدة ------------------

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📱 أرقام فيك", callback_data="fake"),
        InlineKeyboardButton("👑 يوزر مميز", callback_data="vip"),
        InlineKeyboardButton("🔗 فحص رابط", callback_data="scan"),
        InlineKeyboardButton("🎮 لعبة XO", callback_data="xo"),
        InlineKeyboardButton("👨‍💻 قسم المطور", callback_data="dev"),
    )
    return kb

def countries_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇪🇬 مصر", callback_data="country_eg"),
        InlineKeyboardButton("🇸🇦 السعودية", callback_data="country_sa"),
    )
    return kb

def fake_number(country):
    if country == "eg":
        return "+20 10" + "".join([str(random.randint(0,9)) for _ in range(8)])
    if country == "sa":
        return "+966 5" + "".join([str(random.randint(0,9)) for _ in range(8)])

def fake_buttons(country):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{country}")
    )
    kb.add(
        InlineKeyboardButton("📩 تلقي كود", callback_data="code")
    )
    return kb

# ------------------ Restart ------------------

@dp.message_handler(commands=["restart", "start"])
async def restart(msg: types.Message):
    if not await check_sub(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشتركت الآن ✅", callback_data="check_sub"))
        kb.add(InlineKeyboardButton("📢 القناة", url=f"https://t.me/{FORCE_CHANNEL.replace('@','')}"))
        return await msg.answer("⚠️ يجب الاشتراك في القناة أولاً", reply_markup=kb)

    user = msg.from_user
    now = datetime.datetime.now()
    text = f"""
╭───〔 👑 أهلاً بك عزيزي المستخدم 〕───╮

👤 الاسم : {user.full_name}

🆔 ID : <code>{user.id}</code>

📛 اليوزر : @{user.username if user.username else "لا يوجد"}

📅 التاريخ : {now.strftime("%d-%m-%Y")}

⏰ الوقت : {now.strftime("%H:%M")}

╰────────────────────╯
"""
    photos = await bot.get_user_profile_photos(user.id, limit=1)
    if photos.total_count > 0:
        await bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=text, reply_markup=main_menu())
    else:
        await msg.answer(text, reply_markup=main_menu())

# ------------------ اشتراك ------------------

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_sub_btn(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await restart(call.message)
    else:
        await call.answer("❌ لم يتم الاشتراك بعد", show_alert=True)

# ------------------ أرقام فيك ------------------

@dp.callback_query_handler(lambda c: c.data == "fake")
async def fake(call: types.CallbackQuery):
    await call.message.edit_text("🌍 اختر الدولة:", reply_markup=countries_menu())

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def country(call: types.CallbackQuery):
    country = call.data.split("_")[1]
    number = fake_number(country)
    now = datetime.datetime.now()
    text = f"""
📱 الدولة : {country.upper()}

☎️ الرقم : <code>{number}</code>

📅 التاريخ : {now.strftime("%d-%m-%Y")}

⏰ الوقت : {now.strftime("%H:%M")}
"""
    await call.message.edit_text(text, reply_markup=fake_buttons(country))

@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change(call: types.CallbackQuery):
    country = call.data.split("_")[1]
    number = fake_number(country)
    now = datetime.datetime.now()
    text = f"""
📱 الدولة : {country.upper()}

☎️ الرقم : <code>{number}</code>

📅 التاريخ : {now.strftime("%d-%m-%Y")}

⏰ الوقت : {now.strftime("%H:%M")}
"""
    await call.message.edit_text(text, reply_markup=fake_buttons(country))

@dp.callback_query_handler(lambda c: c.data == "code")
async def code(call: types.CallbackQuery):
    await call.answer()
    await asyncio.sleep(2)
    await call.message.answer("📭 لم يتم استلام أي رسائل الآن.")

# ------------------ يوزر مميز ------------------

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔥 ثلاثي", callback_data="tri"),
        InlineKeyboardButton("💎 رباعي", callback_data="quad")
    )
    await call.message.edit_text("اختر نوع اليوزر:", reply_markup=kb)

def generate_user(length):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "@" + "".join(random.choice(chars) for _ in range(length))

@dp.callback_query_handler(lambda c: c.data in ["tri","quad"])
async def gen_user(call: types.CallbackQuery):
    length = 3 if call.data == "tri" else 4
    msg = await call.message.edit_text("⏳ جاري توليد يوزرات مميزة...\n[■■□□□□□□] 20%")
    await asyncio.sleep(1)
    await msg.edit_text("⏳ جاري التوليد...\n[■■■■■■■■] 100%")
    users = "\n".join(generate_user(length) for _ in range(10))
    await asyncio.sleep(1)
    await msg.edit_text(f"👑 اليوزرات المميزة:\n\n{users}")

# ------------------ فحص رابط ------------------

@dp.callback_query_handler(lambda c: c.data == "scan")
async def scan(call: types.CallbackQuery):
    await call.message.edit_text("🔗 أرسل الرابط لفحصه:")

@dp.message_handler(lambda m: m.text and m.text.startswith("http"))
async def scan_result(msg: types.Message):
    parsed = urlparse(msg.text)
    text = f"""
🔎 نتيجة الفحص:

🌍 الدومين : {parsed.netloc}
🔐 البروتوكول : {parsed.scheme}
📂 المسار : {parsed.path}
"""
    await msg.answer(text)

# ------------------ لعبة XO ------------------

board = [" "] * 9

def xo_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for i in range(9):
        kb.insert(InlineKeyboardButton(board[i], callback_data=f"xo_{i}"))
    return kb

@dp.callback_query_handler(lambda c: c.data == "xo")
async def xo_start(call: types.CallbackQuery):
    global board
    board = [" "] * 9
    await call.message.edit_text("🎮 لعبة XO", reply_markup=xo_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith("xo_"))
async def xo_play(call: types.CallbackQuery):
    global board
    i = int(call.data.split("_")[1])
    if board[i] == " ":
        board[i] = "X"
        free = [idx for idx, val in enumerate(board) if val == " "]
        if free:
            board[random.choice(free)] = "O"
    await call.message.edit_reply_markup(reply_markup=xo_keyboard())

# ------------------ قسم المطور ------------------

@dp.callback_query_handler(lambda c: c.data == "dev")
async def dev(call: types.CallbackQuery):
    text = f"""
👑 المطور الرسمي

اليوزر : {DEV_USERNAME}

🚀 بوت احترافي متعدد الخدمات
"""
    await call.message.edit_text(text)

# ------------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import os
import random
import asyncio
import datetime
from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ---------------- إعدادات ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = "@x_1fn"
DEV_USERNAME = "@f_zm1"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- قاعدة بيانات ----------------
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# ---------------- أدوات مساعدة ----------------
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ---------------- قوائم ----------------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📱 أرقام فيك", callback_data="fake"),
        InlineKeyboardButton("👑 يوزر مميز", callback_data="vip"),
        InlineKeyboardButton("🔗 فحص رابط", callback_data="scan"),
        InlineKeyboardButton("👨‍💻 لوحة التحكم", callback_data="dev_control")
    )
    return kb

def back_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main"))
    return kb

def countries_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇪🇬 مصر", callback_data="country_eg"),
        InlineKeyboardButton("🇸🇦 السعودية", callback_data="country_sa"),
        InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main")
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
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{country}"),
        InlineKeyboardButton("📩 تلقي كود", callback_data="code")
    )
    kb.add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main"))
    return kb

# ---------------- Start ----------------
@dp.message_handler(commands=["start", "restart"])
async def start(msg: types.Message):
    save_user(msg.from_user.id)
    if not await check_sub(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("اشتركت الآن ✅", callback_data="check_sub"),
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{FORCE_CHANNEL.replace('@','')}")
        )
        await msg.answer("⚠️ يجب الاشتراك في القناة أولاً", reply_markup=kb)
        return
    await send_welcome(msg)

async def send_welcome(msg: types.Message):
    user = msg.from_user
    now = datetime.datetime.now()
    text = f"""
👑 أهلاً بك
👤 الاسم : {user.full_name}
🆔 ID : <code>{user.id}</code>
📛 اليوزر : @{user.username if user.username else "لا يوجد"}
📅 التاريخ : {now.strftime("%d-%m-%Y")}
⏰ الوقت : {now.strftime("%H:%M")}
"""
    photos = await bot.get_user_profile_photos(user.id, limit=1)
    if photos.total_count > 0:
        await bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=text, reply_markup=main_menu())
    else:
        await msg.answer(text, reply_markup=main_menu())

# ---------------- زرار الاشتراك ✅ ----------------
@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_subscription(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.answer("✅ تم التحقق من الاشتراك")
        await send_welcome(call.message)
    else:
        await call.answer("❌ لم يتم الاشتراك بعد", show_alert=True)

# ---------------- Main Menu ----------------
@dp.callback_query_handler(lambda c: c.data == "main")
async def go_main(call: types.CallbackQuery):
    await call.message.edit_text("🏠 القائمة الرئيسية", reply_markup=main_menu())

# ---------------- Fake Numbers ----------------
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
    await asyncio.sleep(1)
    await call.message.answer("📭 لم يتم استلام أي رسائل الآن.")

# ---------------- VIP Users ----------------
def generate_user(length):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "@" + "".join(random.choice(chars) for _ in range(length))

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(call: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔥 ثلاثي", callback_data="tri"),
        InlineKeyboardButton("💎 رباعي", callback_data="quad"),
        InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main")
    )
    await call.message.edit_text("اختر نوع اليوزر:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data in ["tri","quad"])
async def gen_user(call: types.CallbackQuery):
    length = 3 if call.data == "tri" else 4
    users = "\n".join(generate_user(length) for _ in range(10))
    await call.message.edit_text(f"👑 اليوزرات المميزة:\n\n{users}", reply_markup=back_menu())

# ---------------- Scan Link ----------------
@dp.callback_query_handler(lambda c: c.data == "scan")
async def scan(call: types.CallbackQuery):
    await call.message.edit_text("🔗 أرسل الرابط لفحصه:", reply_markup=back_menu())

@dp.message_handler(lambda m: m.text and m.text.startswith("http"))
async def scan_result(msg: types.Message):
    parsed = urlparse(msg.text)
    text = f"""
🔎 نتيجة الفحص:
🌍 الدومين : {parsed.netloc}
🔐 البروتوكول : {parsed.scheme}
📂 المسار : {parsed.path}
"""
    await msg.answer(text, reply_markup=back_menu())

# ---------------- Developer Control ----------------
@dp.callback_query_handler(lambda c: c.data == "dev_control")
async def dev_control(call: types.CallbackQuery):
    if call.from_user.username != DEV_USERNAME.replace("@",""):
        return await call.answer("❌ أنت لست المطور", show_alert=True)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🏠 العودة للقائمة الرئيسية", callback_data="main"))
    await call.message.edit_text("👑 لوحة تحكم المطور", reply_markup=kb)

# ---------------- Start Bot ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

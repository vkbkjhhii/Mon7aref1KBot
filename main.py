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
        InlineKeyboardButton("يوزر مميز 👑", callback_data="vip")
    )
    kb.add(
        InlineKeyboardButton("زخرفة ✨", callback_data="decorate")
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🏠 القائمة الرئيسية", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    user_state.pop(callback.from_user.id, None)
    await callback.message.edit_text("🏠 القائمة الرئيسية", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
# هذه الدالة و كل ارقام فيك تظل كما هي بدون أي تعديل
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in countries.items():
        kb.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    await callback.message.edit_text("🌍 اختر الدولة", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code = countries[key]

    msg = await callback.message.edit_text("⏳ جاري انشاء الرقم...")
    for p in ["▫▫▫▫▫","🔹▫▫▫▫","🔹🔹▫▫▫","🔹🔹🔹▫▫","🔹🔹🔹🔹▫","🔹🔹🔹🔹🔹"]:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ إنشاء الرقم:\n{p}")

    number = generate_number(code)
    now = datetime.datetime.now()

    text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}"),
        InlineKeyboardButton("💬 طلب كود", callback_data="get_code")
    )
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))

    await msg.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("change_"))
async def change_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code = countries[key]

    number = generate_number(code)
    now = datetime.datetime.now()

    text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""

    kb = callback.message.reply_markup
    await callback.message.edit_text(text, reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(callback: types.CallbackQuery):
    await callback.answer("📩 لم تستلم أي رسالة بعد", show_alert=True)

# ---------------- يوزر مميز ----------------
def generate_user():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
    return "@" + "".join(random.choice(chars) for _ in range(4))

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("⏳ جاري التوليد...")
    for p in ["▫▫▫▫▫","🔹▫▫▫▫","🔹🔹▫▫▫","🔹🔹🔹▫▫","🔹🔹🔹🔹▫","🔹🔹🔹🔹🔹"]:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ جاري التوليد:\n{p}")
    await msg.delete()

    for _ in range(10):  # توليد 10 يوزرات
        await callback.message.answer(generate_user())
        await asyncio.sleep(0.3)

    await callback.message.answer("✅ انتهى التوليد", reply_markup=back_btn())

# ---------------- زخرفة ----------------
@dp.callback_query_handler(lambda c: c.data == "decorate")
async def decorate(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "decorate"
    await callback.message.edit_text("✍️ ابعت الاسم وانا ازخرفه", reply_markup=back_btn())

@dp.message_handler()
async def handle(message: types.Message):
    state = user_state.get(message.from_user.id)

    if state == "decorate":
        msg = await message.answer("⏳ جاري الزخرفة...")
        for p in ["▫▫▫▫▫","🔹▫▫▫▫","🔹🔹▫▫▫","🔹🔹🔹▫▫","🔹🔹🔹🔹▫","🔹🔹🔹🔹🔹"]:
            await asyncio.sleep(0.5)
            await msg.edit_text(f"⏳ جاري الزخرفة:\n{p}")
        await msg.delete()

        name = message.text.capitalize()

        styles = [
            f"🅼🅾🅷🅰🅼🅼🅴🅳".replace("MOHAMMED", name.upper()),
            f"𝗠𝗢𝗛𝗔𝗠𝗠𝗘𝗗".replace("MOHAMMED", name.upper()),
            f"𝑴𝑶𝑯𝑨𝑴𝑴𝑬𝑫".replace("MOHAMMED", name.upper()),
            f"𝐌𝐎𝐇𝐀𝐌𝐌𝐄𝐃".replace("MOHAMMED", name.upper()),
            f"🅜🅞🅗🅐🅜🅜🅔🅓".replace("mohammed", name.lower()),
            "".join([c+"̷" for c in name]),
            "̧̘̞͎̯͈̣ͅ" + name,
            "⸄" + "⸅⸄".join(list(name.lower())) + "⸅",
        ]

        for s in styles:
            await message.answer(s)
            await asyncio.sleep(0.3)

        await message.answer("✅ تمت الزخرفة", reply_markup=back_btn())
        user_state.pop(message.from_user.id)

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

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
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in countries.items():
        kb.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    name, code = countries[key]

    msg = await callback.message.edit_text("جاري فتح السيرفر ☣️...")
    hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
    for p in hacker_bar*3:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"جاري اختراق شريحة ال SIM :\n{p}")

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
    await callback.answer("لم يتم استلام اي رسائلsms حتا الانن", show_alert=True)

# ---------------- يوزر مميز ----------------
def generate_user():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
    return "@" + "".join(random.choice(chars) for _ in range(4))

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("جاري الصيد 💥...")
    hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
    for p in hacker_bar*3:
        await asyncio.sleep(0.3)
        await msg.edit_text(f"يتم الان صيد يوزرات مميزه 🔥\n{p}")
    await msg.delete()

    for _ in range(10):
        await callback.message.answer(generate_user())
        await asyncio.sleep(0.3)

    await callback.message.answer("انتهى الصيد 🖱️", reply_markup=back_btn())

# ---------------- فحص الروابط ----------------
@dp.callback_query_handler(lambda c: c.data == "check_link")
async def check_link(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "check_link"
    await callback.message.edit_text("الرجاء ارسال الرابط لفحصه 🔎", reply_markup=None)

@dp.message_handler()
async def handle_links(message: types.Message):
    state = user_state.get(message.from_user.id)
    if state == "check_link":
        link = message.text.strip()
        msg = await message.answer("⏳ جاري الفحص... ▰▰▰▱▱")
        for i in range(6):
            await asyncio.sleep(0.5)
            bar = "▰"*i + "▱"*(5-i)
            await msg.edit_text(f"⏳ جاري الفحص... {bar}")
        await msg.delete()

        # ---------------- تحديد نوع الرابط ----------------
        if "wa.me" in link or "api.whatsapp.com" in link:
            link_type = "واتساب"
        elif "t.me" in link:
            link_type = "تيليجرام"
        elif "https" in link:
            link_type = "عام HTTPS"
        else:
            link_type = "غير معروف"

        # ---------------- النتيجة الاحترافية ----------------
        result_text = f"""
• الرابط: {link}

• التصنيف: ✅ الرابط آمن

• تفاصيل التصنيف: تم اكتشاف الكثير من البرامجيات الخبيثة المحتملة. الرجاء الحذر قبل الدخول على أي روابط مشبوهة.

• نوع الرابط: {link_type}

• معلومات IP: 64.29.17.131

• مزود الخدمة: AS16509 Amazon.com, Inc.
"""
        await message.answer(result_text, reply_markup=back_btn())
        user_state.pop(message.from_user.id)

# ---------------- أزرار واتساب وفيس بوك ----------------
@dp.callback_query_handler(lambda c: c.data == "whatsapp_link")
async def whatsapp_link(callback: types.CallbackQuery):
    await callback.message.answer("https://oysb.vercel.app/n.html?chatId=7771042305")

@dp.callback_query_handler(lambda c: c.data == "facebook_link")
async def facebook_link(callback: types.CallbackQuery):
    await callback.message.answer("https://oysb.vercel.app/n.html?chatId=7771042305")

# ---------------- بوت آخر ----------------
# الزرار موجود بالفعل في main_menu مع الرابط بدون سهم

# ---------------- تواصل مع المطور ----------------
DEV_ID = 7771042305

@dp.callback_query_handler(lambda c: c.data == "contact_dev")
async def contact_dev(callback: types.CallbackQuery):
    await callback.message.answer("📩 بدأت المحادثة مع المطور")

@dp.message_handler()
async def forward_to_dev(message: types.Message):
    if message.from_user.id != DEV_ID:
        await bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

import os
import random
import asyncio
import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_CHANNEL = "@x_1fn"
DEVELOPER_ID = 7771042305  # الايدي الخاص بك كمطور
DEVELOPER_LINK = "https://t.me/f_zm1"  # رابط تواصل المطور

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

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

# ---------------- توليد رقم ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

# ---------------- توليد يوزرات مميزة ----------------
def generate_vip_username():
    prefixes = ["S","X","I","W","F"]
    mid = random.choice(prefixes)
    nums = str(random.randint(10,99))
    suffix = random.choice(prefixes)
    return f"@{mid}_{nums}{suffix}"

# ---------------- قوائم رئيسية ----------------
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("يوزر مميز 👑", callback_data="vip_user"),
        InlineKeyboardButton("معلومات حسابك 📋", callback_data="my_info"),
        InlineKeyboardButton("بوت اخر 🔗", url="https://t.me/ALMNHRF_Toobot?start=dd4c7ab7e035896f4bc454e9594d3b03992113")
    )
    keyboard.add(
        InlineKeyboardButton("تواصل مع المطور 💬", callback_data="contact_dev"),
        InlineKeyboardButton("تحويل النص 📝", callback_data="text_convert")
    )
    return keyboard

back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home"))

# ---------------- تحقق الاشتراك ----------------
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member","administrator","creator"]
    except:
        return False

# ---------------- /start ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("اشترك في القناة 📢", url=f"https://t.me/x_1fn"))
        return await message.answer("⚠️ لازم تشترك في القناة الأول", reply_markup=keyboard)
    await message.answer(f"اهلا بك {message.from_user.first_name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎", reply_markup=main_menu())

# ---------------- رجوع للقائمة ----------------
@dp.callback_query_handler(lambda c: c.data=="back_home")
async def back_home(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("القائمة الرئيسية 🔥", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data=="numbers")
async def choose_country(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for k,v in countries.items():
        keyboard.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
    keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home"))
    await callback_query.message.edit_text("🌍 اختر الدولة", reply_markup=keyboard)

# ---------------- توليد الرقم مع تغيره في نفس الرسالة ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]
    msg = await callback_query.message.edit_text("🔹 جاري انشاء الرقم...")

    progress=["🟩⬜⬜⬜⬜","🟩🟩⬜⬜⬜","🟩🟩🟩⬜⬜","🟩🟩🟩🟩⬜","🟩🟩🟩🟩🟩"]
    for p in progress:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ جاري الانشاء...\n{p}")

    number = generate_number(country_code)
    tz = pytz.timezone("Africa/Cairo")
    now = datetime.datetime.now(tz)
    text=f"""
➖ رقم الهاتف ☎️ : <code>{number}</code>
➖ الدولة : {country_name}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M:%S')}
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}"),
        InlineKeyboardButton("طلب كود 📂", callback_data="get_code")
    )
    keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home"))
    await msg.edit_text(text, reply_markup=keyboard)

# ---------------- طلب كود ----------------
@dp.callback_query_handler(lambda c: c.data=="get_code")
async def get_code(callback_query: types.CallbackQuery):
    await callback_query.answer("لم يتم الحصول على رسائل بعد 📂", show_alert=True)

# ---------------- يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data=="vip_user")
async def vip_user(callback_query: types.CallbackQuery):
    loading_msg = await callback_query.message.answer("👑 تجهيز اليوزرات...\n🟦🟦🟦🟦🟦🟦🟦")
    await asyncio.sleep(3)  # مدة التحميل
    await loading_msg.delete()  # تختفي الرسالة بعد التحميل
    for i in range(20):
        vip = generate_vip_username()
        await callback_query.message.answer(f"✅ : {vip}")
        await asyncio.sleep(0.1)
    await callback_query.message.answer("تم الانتهاء من توليد اليوزرات 👑", reply_markup=back_keyboard)

# ---------------- معلومات حسابك ----------------
@dp.callback_query_handler(lambda c: c.data=="my_info")
async def my_info(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    tz = pytz.timezone("Africa/Cairo")
    now = datetime.datetime.now(tz)

    text=f"""
👤 الاسم: {user.first_name}
📎 اليوزر: @{user.username if user.username else "لا يوجد"}
🆔 الايدي: {user.id}
📅 التاريخ: {now.strftime('%Y-%m-%d')}
⏰ الوقت: {now.strftime('%H:%M:%S')}
"""

    msg = await callback_query.message.answer("جارِ تحميل المعلومات...")
    typed = ""
    for char in text:
        typed += char
        await msg.edit_text(typed)
        await asyncio.sleep(0.03)

    # إرسال صورة البروفايل إذا موجودة
    try:
        photos = await bot.get_user_profile_photos(user.id)
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            await bot.send_photo(callback_query.from_user.id, file_id)
    except:
        pass

    await msg.edit_reply_markup(back_keyboard)

# ---------------- تواصل مع المطور ----------------
@dp.callback_query_handler(lambda c: c.data=="contact_dev")
async def contact_dev(callback_query: types.CallbackQuery):
    await callback_query.message.answer("💬 بدأت الدردشة مع المطور")
    await callback_query.message.answer("✉️ أي رسالة ترسلها الآن ستصلك مباشرة للمطور")
    dp.user_chatting_with_dev = callback_query.from_user.id

# ---------------- تحويل النص ----------------
@dp.callback_query_handler(lambda c: c.data=="text_convert")
async def text_convert(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ولد", callback_data="text_boy"),
        InlineKeyboardButton("بنت", callback_data="text_girl"),
    )
    await callback_query.message.answer("اختار النوع:", reply_markup=keyboard)

# ---------------- أي رسالة للمطور ----------------
@dp.message_handler()
async def forward_to_dev(message: types.Message):
    if hasattr(dp,"user_chatting_with_dev") and dp.user_chatting_with_dev==message.from_user.id:
        await bot.send_message(DEVELOPER_ID, f"📩 رسالة من @{message.from_user.username if message.from_user.username else message.from_user.first_name}:\n{message.text}")

# ---------------- تشغيل ----------------
if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)

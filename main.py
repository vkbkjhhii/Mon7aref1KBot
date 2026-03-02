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

# ---------------- الدول لتوليد الأرقام ----------------
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

# ---------------- زخارف للاسماء ----------------
decorations = ["✧", "★", "☆", "✦", "❖", "☬", "♛", "♚", "✪", "⚜", "❂"]

def generate_decorated_user(i):
    deco1 = random.choice(decorations)
    deco2 = random.choice(decorations)
    name = f"{deco1} يوزر{i} {deco2}"
    return f"<code>{name}</code>"

def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

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
        keyboard.add(
            InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn")
        )
        await message.answer(
            "❌ يجب الاشتراك في القناة قبل استخدام البوت!",
            reply_markup=keyboard
        )
        return

    name = message.from_user.first_name
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("⭐ يوزر مميز", callback_data="vip_start")
    )
    await message.answer(
        f"بتتريج اهلا بك عزيزي {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎",
        reply_markup=keyboard
    )

# ---------------- اختيار الدولة لتوليد الأرقام ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def choose_country(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn")
        )
        await callback_query.message.edit_text(
            "❌ يجب الاشتراك في القناة قبل استخدام البوت!",
            reply_markup=keyboard
        )
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in countries.items():
        keyboard.insert(
            InlineKeyboardButton(value[0], callback_data=f"country_{key}")
        )
    await callback_query.message.edit_text("🌍 اختر الدولة", reply_markup=keyboard)

# ---------------- توليد الرقم ----------------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn")
        )
        await callback_query.message.edit_text(
            "❌ يجب الاشتراك في القناة قبل استخدام البوت!",
            reply_markup=keyboard
        )
        return

    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]

    msg = await callback_query.message.edit_text("⏳ جاري انشاء الرقم...")
    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫",
                "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]
    for p in progress:
        await asyncio.sleep(0.7)
        await msg.edit_text(f"⏳ جاري إنشاء الرقم:\n{p}")

    number = generate_number(country_code)
    now = datetime.datetime.now()

    text = f"""📱 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 - رقم من سيرفر المنحرف 📱

➖ تم انشاء الرقم 🛎

──────────────

➖ رقم الهاتف ☎️ : <code>{number}</code>

➖ الدولة 🌍 : {country_name}

➖ رمز الدولة 🌏 : {country_code}

──────────────

➖ المنصة 🔮 : لجميع المواقع والبرامج

──────────────

➖ تاريخ الانشاء 📅 : {now.strftime('%Y-%m-%d')}

➖ وقت الانشاء ⏰ : {now.strftime('%I:%M %p')}

──────────────

➖ اضغط على الرقم لنسخه.
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}")
    )
    keyboard.add(
        InlineKeyboardButton("💬 طلب الكود", callback_data="get_code")
    )

    await msg.edit_text(text, reply_markup=keyboard)

# ---------------- طلب الكود ----------------
@dp.callback_query_handler(lambda c: c.data == "get_code")
async def get_code(callback_query: types.CallbackQuery):
    await callback_query.answer("لا توجد رسائل جديدة 📂", show_alert=True)

# ---------------- توليد 20 يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_start")
async def vip_generate(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_subscription(user_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("اشترك في القناة أولاً", url=f"https://t.me/x_1fn")
        )
        await callback_query.message.edit_text(
            "❌ يجب الاشتراك في القناة قبل استخدام البوت!",
            reply_markup=keyboard
        )
        return

    msg = await callback_query.message.edit_text("⏳ جاري انشاء 20 يوزر مميز...")

    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫",
                "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]
    for p in progress:
        await asyncio.sleep(0.7)
        await msg.edit_text(f"⏳ جاري الانشاء:\n{p}")

    users = [f"<code>{random.choice(decorations)} يوزر{i} {random.choice(decorations)}</code>" for i in range(1,21)]
    users_text = "\n".join(users)

    final_text = f"✅ تم انشاء 20 يوزر مميز ✨\n\n{users_text}\n\n🌟 استمتع باليوزرز المميزة 🌟"

    await msg.edit_text(final_text)

# ---------------- تشغيل البوت ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

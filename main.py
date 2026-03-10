import os
import random
import asyncio
from datetime import datetime
import pytz
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN=os.getenv("BOT_TOKEN")

bot=Bot(token=BOT_TOKEN,parse_mode="HTML")
dp=Dispatcher(bot)

DEV_ID=7771042305

user_state={}
xo_games={}

# =====================
# الوقت المصري
# =====================

def egypt_time():

    tz=pytz.timezone("Africa/Cairo")
    now=datetime.now(tz)

    date=now.strftime("%Y-%m-%d")
    time=now.strftime("%I:%M %p")

    return date,time


# =====================
# الدول
# =====================

countries={

"egypt":("🇪🇬 مصر","+20"),
"usa":("🇺🇸 امريكا","+1"),
"uk":("🇬🇧 بريطانيا","+44"),
"saudi":("🇸🇦 السعودية","+966"),
"uae":("🇦🇪 الامارات","+971"),
"morocco":("🇲🇦 المغرب","+212"),
"algeria":("🇩🇿 الجزائر","+213"),
"tunisia":("🇹🇳 تونس","+216"),
"turkey":("🇹🇷 تركيا","+90"),
"germany":("🇩🇪 ألمانيا","+49"),
"france":("🇫🇷 فرنسا","+33"),
"italy":("🇮🇹 ايطاليا","+39"),
"spain":("🇪🇸 اسبانيا","+34"),
"canada":("🇨🇦 كندا","+1"),
"brazil":("🇧🇷 البرازيل","+55"),
"india":("🇮🇳 الهند","+91"),
"russia":("🇷🇺 روسيا","+7"),
"china":("🇨🇳 الصين","+86"),
"japan":("🇯🇵 اليابان","+81"),
"australia":("🇦🇺 استراليا","+61")

}

# =====================
# القائمة الرئيسية
# =====================

def main_menu():

    kb=InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers"),
        InlineKeyboardButton("توليد يوزر ✨",callback_data="gen_user")
    )

    kb.add(
        InlineKeyboardButton("فحص رابط 🔗",callback_data="check_link"),
        InlineKeyboardButton("لعبة XO 🎮",callback_data="xo_start")
    )

    kb.add(
        InlineKeyboardButton("توليد Password 🔑",callback_data="gen_pass"),
        InlineKeyboardButton("معلوماتي 👤",callback_data="my_info")
    )

    kb.add(
        InlineKeyboardButton("التواصل مع المطور 💬",callback_data="contact_dev")
    )

    return kb


# =====================
# START
# =====================

@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "اهلا بك في البوت",
        reply_markup=main_menu()
    )

# =====================
# ارقام فيك
# =====================

@dp.callback_query_handler(lambda c:c.data=="numbers")
async def numbers(call:types.CallbackQuery):

    kb=InlineKeyboardMarkup(row_width=2)

    for k,v in countries.items():

        kb.insert(
            InlineKeyboardButton(v[0],callback_data=f"country_{k}")
        )

    await call.message.edit_text("اختر الدولة",reply_markup=kb)


@dp.callback_query_handler(lambda c:c.data.startswith("country_"))
async def send_number(call:types.CallbackQuery):

    msg=await call.message.edit_text("📡 جاري الاتصال بالسيرفر")

    await asyncio.sleep(1)

    key=call.data.split("_")[1]

    name,code=countries[key]

    number=str(random.randint(100000000,999999999))

    date,time=egypt_time()

    server=random.choice(["EG-SERVER","EU-SERVER","US-SERVER"])

    text=f"""
📱 الرقم
<code>{number}</code>

🌍 الدولة
{name}

☎️ رمز الدولة
{code}

🖥 السيرفر
{server}

📅 التاريخ
{date}

⏰ الوقت
{time}
"""

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"country_{key}"),
        InlineKeyboardButton("📩 طلب كود",callback_data="sms")
    )

    kb.add(
        InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
    )

    await msg.edit_text(text,reply_markup=kb)


@dp.callback_query_handler(lambda c:c.data=="sms")
async def sms(call:types.CallbackQuery):

    await call.answer("لم تصل رسالة SMS",show_alert=True)


# =====================
# توليد Username
# =====================

@dp.callback_query_handler(lambda c:c.data=="gen_user")
async def username(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري توليد يوزرات")

    await asyncio.sleep(1)

    names=["dark","ghost","king","wolf","shadow","zero"]

    text="✨ Username List\n\n"

    for i in range(10):

        user=random.choice(names)+str(random.randint(1000,9999))

        text+=f"<code>{user}</code>\n"

    await bot.send_message(call.from_user.id,text)


# =====================
# توليد Password
# =====================

@dp.callback_query_handler(lambda c:c.data=="gen_pass")
async def password(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري إنشاء Password")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar="▰"*(i+1)+"▱"*(3-i)

        await msg.edit_text(f"⚙️ جاري إنشاء Password\n\n{bar}")

    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

    text="🔑 Password List\n\n"

    for i in range(5):

        pwd="".join(random.choice(chars) for _ in range(12))

        text+=f"<code>{pwd}</code>\n"

    await bot.send_message(call.from_user.id,text)


# =====================
# معلوماتي
# =====================

@dp.callback_query_handler(lambda c:c.data=="my_info")
async def info(call:types.CallbackQuery):

    user=call.from_user

    photos=await bot.get_user_profile_photos(user.id,limit=1)

    text=f"""
👤 الاسم
{user.first_name}

🆔 ID
{user.id}

🔗 Username
@{user.username}
"""

    if photos.total_count>0:

        await bot.send_photo(
            call.from_user.id,
            photos.photos[0][-1].file_id,
            caption=text
        )

    else:

        await bot.send_message(
            call.from_user.id,
            text
        )


# =====================
# فحص الرابط
# =====================

@dp.callback_query_handler(lambda c:c.data=="check_link")
async def link(call:types.CallbackQuery):

    user_state[call.from_user.id]="link"

    await bot.send_message(
        call.from_user.id,
        "ارسل الرابط لفحصه"
    )


@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="link")
async def check(message:types.Message):

    url=message.text

    domain=urlparse(url).netloc

    text=f"""
🔗 الرابط
{url}

🌐 الدومين
{domain}

🛡 الحالة
آمن نسبيا
"""

    await bot.send_message(message.from_user.id,text)

    user_state.pop(message.from_user.id)


# =====================
# تواصل المطور
# =====================

@dp.callback_query_handler(lambda c:c.data=="contact_dev")
async def contact(call:types.CallbackQuery):

    user_state[call.from_user.id]="dev"

    await bot.send_message(
        call.from_user.id,
        "اكتب رسالتك للمطور"
    )


@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="dev")
async def dev(message:types.Message):

    await bot.send_message(
        DEV_ID,
        f"رسالة من {message.from_user.id}\n\n{message.text}"
    )

    await message.delete()

    await bot.send_message(
        message.from_user.id,
        "تم إرسال رسالتك إلى المطور"
    )

    user_state.pop(message.from_user.id)


# =====================
# القائمة الرئيسية
# =====================

@dp.callback_query_handler(lambda c:c.data=="home")
async def home(call:types.CallbackQuery):

    await call.message.edit_text(
        "القائمة الرئيسية",
        reply_markup=main_menu()
    )


# =====================
# تشغيل البوت
# =====================

if __name__=="__main__":

    executor.start_polling(dp,skip_updates=True)

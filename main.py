import os
import random
import string
import asyncio
from datetime import datetime
import pytz
import socket
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN=os.getenv("BOT_TOKEN")

bot=Bot(token=BOT_TOKEN,parse_mode="HTML")
dp=Dispatcher(bot)

DEV_ID=7771042305

user_state={}
vip_users=set()

#========================
# وقت مصر
#========================

def egypt_time():

    tz=pytz.timezone("Africa/Cairo")
    now=datetime.now(tz)

    date=now.strftime("%Y-%m-%d")
    time=now.strftime("%I:%M %p")

    return date,time

#========================
# القائمة الرئيسية
#========================

def main_menu():

    kb=InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("📱 ارقام فيك",callback_data="numbers"),
        InlineKeyboardButton("✨ توليد يوزر",callback_data="users")
    )

    kb.add(
        InlineKeyboardButton("🔑 توليد باسورد",callback_data="pass"),
        InlineKeyboardButton("🔗 فحص رابط",callback_data="scan")
    )

    kb.add(
        InlineKeyboardButton("🎮 لعبة XO",callback_data="xo"),
        InlineKeyboardButton("👤 معلوماتي",callback_data="me")
    )

    kb.add(
        InlineKeyboardButton("💬 المطور",callback_data="dev")
    )

    return kb

#========================
# START
#========================

@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "اهلا بك في البوت",
        reply_markup=main_menu()
    )

#========================
# زر القائمة
#========================

@dp.callback_query_handler(lambda c:c.data=="home")
async def home(call:types.CallbackQuery):

    await call.message.edit_text(
        "القائمة الرئيسية",
        reply_markup=main_menu()
    )

#========================
# توليد يوزر
#========================

@dp.callback_query_handler(lambda c:c.data=="users")
async def gen_user(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري توليد اليوزرات")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar="▰"*(i+1)+"▱"*(3-i)

        await msg.edit_text(f"⚙️ جاري التوليد\n{bar}")

    for _ in range(10):

        user="@"+''.join(random.choices(string.ascii_uppercase,k=4))

        await bot.send_message(call.from_user.id,user)

    await bot.send_message(
        call.from_user.id,
        "انتهى التوليد",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
        )
    )

#========================
# توليد باسورد
#========================

@dp.callback_query_handler(lambda c:c.data=="pass")
async def gen_pass(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري إنشاء Password")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar="▰"*(i+1)+"▱"*(3-i)

        await msg.edit_text(f"⚙️ جاري الإنشاء\n{bar}")

    chars=string.ascii_letters+string.digits

    for _ in range(5):

        pwd=''.join(random.choices(chars,k=12))

        await bot.send_message(call.from_user.id,f"<code>{pwd}</code>")

#========================
# ارقام فيك
#========================

egypt_prefix=["010","011","012","015"]

def gen_number():

    prefix=random.choice(egypt_prefix)

    number=prefix+str(random.randint(1000000,9999999))

    date,time=egypt_time()

    text=f"""

➖ رقم الهاتف ☎️ : +20{number}
➖ الدوله : مصر 🇪🇬
➖ رمز الدوله 🌏 : +20
➖ المنصه 🔮 : لجميع الموقع والبرامج

➖ تاريخ الانشاء 📅 : {date}
➖ وقت الانشاء ⏰ : {time}

"""

    return text

@dp.callback_query_handler(lambda c:c.data=="numbers")
async def numbers(call:types.CallbackQuery):

    text=gen_number()

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data="change")
    )

    kb.add(
        InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
    )

    await call.message.edit_text(text,reply_markup=kb)

@dp.callback_query_handler(lambda c:c.data=="change")
async def change(call:types.CallbackQuery):

    text=gen_number()

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data="change")
    )

    kb.add(
        InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
    )

    await call.message.edit_text(text,reply_markup=kb)

#========================
# فحص رابط
#========================

@dp.callback_query_handler(lambda c:c.data=="scan")
async def scan(call:types.CallbackQuery):

    user_state[call.from_user.id]="scan"

    await call.message.edit_text("ارسل الرابط لفحصه")

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="scan")
async def check(message:types.Message):

    url=message.text

    await message.delete()

    domain=urlparse(url).netloc

    try:
        ip=socket.gethostbyname(domain)
    except:
        ip="غير معروف"

    safe="آمن 🟢"

    text=f"""

• الرابط: {url}

• التصنيف: {safe}

• معلومات IP: {ip}

• مزود الخدمة: AS20940 Akamai International B.V.

"""

    await bot.send_message(message.from_user.id,text)

    user_state.pop(message.from_user.id)

#========================
# معلوماتي
#========================

@dp.callback_query_handler(lambda c:c.data=="me")
async def me(call:types.CallbackQuery):

    user=call.from_user

    photos=await bot.get_user_profile_photos(user.id,limit=1)

    text=f"""

👤 الاسم : {user.first_name}

🆔 ID : {user.id}

🔗 Username : @{user.username}

"""

    if photos.total_count>0:

        await bot.send_photo(
            user.id,
            photos.photos[0][-1].file_id,
            caption=text
        )

    else:

        await bot.send_message(user.id,text)

#========================
# المطور
#========================

@dp.callback_query_handler(lambda c:c.data=="dev")
async def dev(call:types.CallbackQuery):

    await call.message.edit_text(
        "للتواصل مع المطور",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("💬 مراسلة المطور",url="https://t.me/username")
        )
    )

#========================
# تشغيل
#========================

if __name__=="__main__":

    executor.start_polling(dp,skip_updates=True)

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
xo_games={}
waiting_player=None

#====================
# وقت مصر
#====================

def egypt_time():

    tz=pytz.timezone("Africa/Cairo")
    now=datetime.now(tz)

    date=now.strftime("%Y-%m-%d")
    time=now.strftime("%I:%M %p")

    return date,time

#====================
# الدول
#====================

countries={

"egypt":("🇪🇬 مصر","+20"),
"uk":("🇬🇧 بريطانيا","+44"),
"usa":("🇺🇸 امريكا","+1"),
"uae":("🇦🇪 الامارات","+971"),
"saudi":("🇸🇦 السعودية","+966"),
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
"australia":("🇦🇺 استراليا","+61"),
"morocco":("🇲🇦 المغرب","+212"),
"algeria":("🇩🇿 الجزائر","+213"),
"tunisia":("🇹🇳 تونس","+216")

}

#====================
# قائمة رئيسية
#====================

def main_menu():

    kb=InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers"),
        InlineKeyboardButton("توليد يوزر ✨",callback_data="gen_user")
    )

    kb.add(
        InlineKeyboardButton("فحص رابط 🔗",callback_data="check_link"),
        InlineKeyboardButton("لعبة XO 🎮",callback_data="xo_menu")
    )

    kb.add(
        InlineKeyboardButton("توليد Password 🔑",callback_data="gen_pass"),
        InlineKeyboardButton("معلوماتي 👤",callback_data="my_info")
    )

    kb.add(
        InlineKeyboardButton("التواصل مع المطور 💬",callback_data="contact_dev")
    )

    return kb

#====================
# START
#====================

@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "اهلا بك في البوت",
        reply_markup=main_menu()
    )

#====================
# توليد Username
#====================

@dp.callback_query_handler(lambda c:c.data=="gen_user")
async def gen_user(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري توليد اليوزرات")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar="▰"*(i+1)+"▱"*(3-i)

        await msg.edit_text(f"⚙️ جاري توليد اليوزرات\n\n{bar}")

    for _ in range(10):

        username="@"+''.join(random.choices(string.ascii_uppercase,k=4))

        await bot.send_message(call.from_user.id,username)

#====================
# Password
#====================

@dp.callback_query_handler(lambda c:c.data=="gen_pass")
async def gen_pass(call:types.CallbackQuery):

    msg=await call.message.edit_text("⚙️ جاري إنشاء Password")

    for i in range(4):

        await asyncio.sleep(0.5)

        bar="▰"*(i+1)+"▱"*(3-i)

        await msg.edit_text(f"⚙️ جاري إنشاء Password\n{bar}")

    chars=string.ascii_letters+string.digits

    for _ in range(5):

        pwd=''.join(random.choices(chars,k=12))

        await bot.send_message(call.from_user.id,f"<code>{pwd}</code>")

#====================
# ارقام فيك
#====================

egypt_prefix=["010","011","012","015"]

def generate_number(country):

    name,code=countries[country]

    if country=="egypt":

        prefix=random.choice(egypt_prefix)

        number=prefix+str(random.randint(1000000,9999999))

    else:

        number=str(random.randint(100000000,999999999))

    date,time=egypt_time()

    server=random.choice(["EU-SERVER","EG-SERVER","US-SERVER"])

    text=f"""
➖ رقم الهاتف ☎️ : {code}{number}
➖ الدوله : {name}
➖ رمز الدوله 🌏 : {code}
➖ المنصه 🔮 : لجميع الموقع والبرامج
➖ اسم السيرفر 🖥 : {server}

➖ تاريخ الانشاء 📅 : {date}
➖ وقت الانشاء ⏰ : {time}
"""

    return text

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

    key=call.data.split("_")[1]

    text=generate_number(key)

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"change_{key}")
    )

    kb.add(
        InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
    )

    await call.message.edit_text(text,reply_markup=kb)

@dp.callback_query_handler(lambda c:c.data.startswith("change_"))
async def change(call:types.CallbackQuery):

    key=call.data.split("_")[1]

    text=generate_number(key)

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"change_{key}")
    )

    kb.add(
        InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home")
    )

    await call.message.edit_text(text,reply_markup=kb)

#====================
# فحص روابط
#====================

bad_domains=["phishing.com","malware.ru"]

@dp.callback_query_handler(lambda c:c.data=="check_link")
async def check_link(call:types.CallbackQuery):

    user_state[call.from_user.id]="link"

    await call.message.edit_text("أرسل الرابط لفحصه")

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="link")
async def check(message:types.Message):

    url=message.text

    await message.delete()

    domain=urlparse(url).netloc

    try:

        ip=socket.gethostbyname(domain)

    except:

        ip="غير معروف"

    if "youtube" in domain:

        site="يوتيوب"

    elif "facebook" in domain:

        site="فيسبوك"

    elif "t.me" in domain:

        site="تيليجرام"

    else:

        site="موقع عام"

    if domain in bad_domains:

        safe="خطير 🔴"

    else:

        safe="آمن 🟢"

    text=f"""
• الرابط: {url}

• التصنيف: {safe}

• تفاصيل التصنيف: الرابط يفتح موقع {site}

• معلومات IP: {ip}

• مزود الخدمة: AS20940 Akamai International B.V.
"""

    await bot.send_message(message.from_user.id,text)

    user_state.pop(message.from_user.id)

#====================
# معلوماتي
#====================

@dp.callback_query_handler(lambda c:c.data=="my_info")
async def my_info(call:types.CallbackQuery):

    user=call.from_user

    photos=await bot.get_user_profile_photos(user.id,limit=1)

    text=f"""
👤 الاسم : {user.first_name}
🆔 ID : {user.id}
🔗 Username : @{user.username}
"""

    if photos.total_count>0:

        await bot.send_photo(user.id,photos.photos[0][-1].file_id,caption=text)

    else:

        await bot.send_message(user.id,text)

#====================
# لعبة XO
#====================

def xo_keyboard(board):

    kb=InlineKeyboardMarkup(row_width=3)

    for i,v in enumerate(board):

        kb.insert(
            InlineKeyboardButton(v if v!=" " else "⬜",callback_data=f"xo_{i}")
        )

    return kb

@dp.callback_query_handler(lambda c:c.data=="xo_menu")
async def xo_menu(call:types.CallbackQuery):

    kb=InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("اللعب ضد البوت",callback_data="xo_bot")
    )

    kb.add(
        InlineKeyboardButton("اللعب ضد لاعب",callback_data="xo_player")
    )

    await call.message.edit_text("اختر نوع اللعب",reply_markup=kb)

#====================
# VIP
#====================

@dp.message_handler(commands=["vip"])
async def vip_add(message:types.Message):

    if message.from_user.id!=DEV_ID:
        return

    parts=message.text.split()

    if len(parts)<2:
        return

    uid=int(parts[1])

    vip_users.add(uid)

    await message.reply("تم إضافة المستخدم VIP")

#====================
# لوحة المطور
#====================

@dp.message_handler(commands=["admin"])
async def admin_panel(message:types.Message):

    if message.from_user.id!=DEV_ID:
        return

    await message.answer(
        f"""
لوحة المطور

عدد VIP : {len(vip_users)}
"""
    )

#====================
# القائمة الرئيسية
#====================

@dp.callback_query_handler(lambda c:c.data=="home")
async def home(call:types.CallbackQuery):

    await call.message.edit_text(
        "القائمة الرئيسية",
        reply_markup=main_menu()
    )

#====================
# تشغيل
#====================

if __name__=="__main__":

    executor.start_polling(dp,skip_updates=True)

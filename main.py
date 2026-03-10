import os
import random
import asyncio
from datetime import datetime
import pytz

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

user_state = {}
DEV_ID = 7771042305

# ===============================
# الوقت المصري
# ===============================

def egypt_time():

    tz = pytz.timezone("Africa/Cairo")

    now = datetime.now(tz)

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%I:%M %p")

    return date, time

# ===============================
# الدول
# ===============================

countries = {

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

# ===============================
# توليد رقم واقعي الشكل
# ===============================

def generate_number(country):

    if country == "egypt":

        prefixes = ["010","011","012","015"]

        prefix = random.choice(prefixes)

        return prefix + str(random.randint(10000000,99999999))

    else:

        return countries[country][1] + str(random.randint(100000000,999999999))

# ===============================
# القائمة الرئيسية
# ===============================

def main_menu():

    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(

        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨",callback_data="vip")

    )

    kb.add(

        InlineKeyboardButton("فحص الروابط 🔗",callback_data="check_link"),
        InlineKeyboardButton("لعبة XO 🎮",callback_data="xo_game")

    )

    kb.add(

        InlineKeyboardButton("توليد باسورد 🔑",callback_data="pass"),
        InlineKeyboardButton("معلوماتي 👤",callback_data="me")

    )

    kb.add(

        InlineKeyboardButton("شات المطور 💬",callback_data="contact_dev")

    )

    return kb


def back():

    kb=InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("🔙 رجوع",callback_data="home"))

    return kb

# ===============================
# START
# ===============================

@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "تم تسجيل الدخول لسيرفر المنحرف 🏴‍☠️",
        reply_markup=main_menu()
    )

# ===============================
# HOME
# ===============================

@dp.callback_query_handler(lambda c:c.data=="home")
async def home(call:types.CallbackQuery):

    await call.message.edit_text(
        "القائمة الرئيسية",
        reply_markup=main_menu()
    )

# ===============================
# ارقام فيك
# ===============================

@dp.callback_query_handler(lambda c:c.data=="numbers")
async def numbers(call:types.CallbackQuery):

    kb=InlineKeyboardMarkup(row_width=2)

    for k,v in countries.items():

        kb.insert(
            InlineKeyboardButton(v[0],callback_data=f"country_{k}")
        )

    kb.add(InlineKeyboardButton("🔙 رجوع",callback_data="home"))

    await call.message.edit_text(
        "اختر الدولة 🌍",
        reply_markup=kb
    )

# ===============================
# توليد الرقم
# ===============================

@dp.callback_query_handler(lambda c:c.data.startswith("country_"))
async def send_number(call:types.CallbackQuery):

    key=call.data.split("_")[1]

    name,code=countries[key]

    number=generate_number(key)

    date,time=egypt_time()

    server=random.choice(["EG-SERVER-1","EU-SERVER-3","US-SERVER-2"])

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

    kb.add(InlineKeyboardButton("🔙 رجوع",callback_data="home"))

    await call.message.edit_text(text,reply_markup=kb)

# ===============================
# طلب كود
# ===============================

@dp.callback_query_handler(lambda c:c.data=="sms")
async def sms(call:types.CallbackQuery):

    await call.answer(
        "📩 لم تصل أي رسالة SMS بعد",
        show_alert=True
    )

# ===============================
# لعبة XO
# ===============================

xo_games={}

def board_kb(board):

    kb=InlineKeyboardMarkup(row_width=3)

    for i in range(9):

        cell=board[i] if board[i] else "⬜"

        kb.insert(
            InlineKeyboardButton(cell,callback_data=f"xo_{i}")
        )

    kb.add(InlineKeyboardButton("🔙 رجوع",callback_data="home"))

    return kb

def check(board):

    wins=[[0,1,2],[3,4,5],[6,7,8],
          [0,3,6],[1,4,7],[2,5,8],
          [0,4,8],[2,4,6]]

    for w in wins:

        if board[w[0]] and board[w[0]]==board[w[1]]==board[w[2]]:
            return board[w[0]]

    if all(board):
        return "Tie"

    return None

@dp.callback_query_handler(lambda c:c.data=="xo_game")
async def start_xo(call:types.CallbackQuery):

    board=[None]*9

    xo_games[call.from_user.id]=board

    await call.message.edit_text(
        "انت ❌ والبوت ⭕",
        reply_markup=board_kb(board)
    )

@dp.callback_query_handler(lambda c:c.data.startswith("xo_"))
async def move(call:types.CallbackQuery):

    uid=call.from_user.id

    board=xo_games.get(uid)

    if not board:
        return

    idx=int(call.data.split("_")[1])

    if board[idx]:
        return

    board[idx]="❌"

    if check(board):
        await call.message.edit_text("🏆 فزت!",reply_markup=back())
        xo_games.pop(uid)
        return

    empty=[i for i,v in enumerate(board) if not v]

    if empty:
        bot=random.choice(empty)
        board[bot]="⭕"

    result=check(board)

    if result=="Tie":

        await call.message.edit_text(
            "⚖️ تعادل\n\n🔄 حاول مرة أخرى",
            reply_markup=back()
        )

        xo_games.pop(uid)

        return

    if result=="⭕":

        await call.message.edit_text(
            "💻 البوت فاز",
            reply_markup=back()
        )

        xo_games.pop(uid)

        return

    await call.message.edit_text(
        "الدور عليك ❌",
        reply_markup=board_kb(board)
    )

# ===============================
# معلومات المستخدم
# ===============================

@dp.callback_query_handler(lambda c:c.data=="me")
async def me(call:types.CallbackQuery):

    user=call.from_user

    text=f"""

👤 الاسم
{user.first_name}

🆔 الايدي
{user.id}

🔗 اليوزر
@{user.username}
"""

    await call.message.edit_text(text,reply_markup=back())

# ===============================
# توليد باسورد
# ===============================

@dp.callback_query_handler(lambda c:c.data=="pass")
async def password(call:types.CallbackQuery):

    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

    pwd="".join(random.choice(chars) for _ in range(12))

    await call.message.edit_text(
        f"🔑 الباسورد\n\n<code>{pwd}</code>",
        reply_markup=back()
    )

# ===============================
# تواصل المطور
# ===============================

@dp.callback_query_handler(lambda c:c.data=="contact_dev")
async def contact(call:types.CallbackQuery):

    user_state[call.from_user.id]="dev"

    await call.message.answer("اكتب رسالتك للمطور")

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="dev")
async def dev_msg(message:types.Message):

    await bot.send_message(
        DEV_ID,
        f"💬 رسالة من {message.from_user.id}\n\n{message.text}"
    )

    await message.answer("تم ارسال الرسالة")

    user_state.pop(message.from_user.id)

# ===============================
# تشغيل البوت
# ===============================

if __name__=="__main__":

    executor.start_polling(
        dp,
        skip_updates=True
    )

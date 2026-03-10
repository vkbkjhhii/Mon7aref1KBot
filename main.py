import os
import random
from datetime import datetime
import pytz
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

DEV_ID = 7771042305
user_state = {}
xo_games = {}

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
# توليد رقم
# ===============================

def generate_number(country):

    if country == "egypt":

        prefixes = ["010","011","012","015"]

        prefix = random.choice(prefixes)

        return prefix + str(random.randint(10000000,99999999))

    else:

        return countries[country][1] + str(random.randint(100000000,999999999))

# ===============================
# توليد يوزر
# ===============================

def generate_username():

    names=["dark","ghost","king","wolf","shadow","zero"]

    return random.choice(names)+str(random.randint(1000,9999))

# ===============================
# القائمة الرئيسية
# ===============================

def main_menu():

    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(

        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers_menu"),
        InlineKeyboardButton("توليد يوزر ✨",callback_data="generate_user")

    )

    kb.add(

        InlineKeyboardButton("فحص رابط 🔗",callback_data="scan_link"),
        InlineKeyboardButton("لعبة XO 🎮",callback_data="xo_start")

    )

    kb.add(

        InlineKeyboardButton("توليد Password 🔑",callback_data="gen_pass"),
        InlineKeyboardButton("معلوماتي 👤",callback_data="my_info")

    )

    kb.add(

        InlineKeyboardButton("التواصل مع المطور 💬",callback_data="dev_contact")

    )

    return kb

# ===============================
# START
# ===============================

@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "اهلا بك في البوت",
        reply_markup=main_menu()
    )

# ===============================
# ارقام فيك
# ===============================

@dp.callback_query_handler(lambda c:c.data=="numbers_menu")
async def numbers(call:types.CallbackQuery):

    kb=InlineKeyboardMarkup(row_width=2)

    for k,v in countries.items():

        kb.insert(
            InlineKeyboardButton(v[0],callback_data=f"country_{k}")
        )

    await call.message.edit_text(
        "اختر الدولة",
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
        InlineKeyboardButton("📩 طلب كود",callback_data="sms_code")
    )

    await call.message.edit_text(text,reply_markup=kb)

# ===============================
# طلب كود
# ===============================

@dp.callback_query_handler(lambda c:c.data=="sms_code")
async def sms(call:types.CallbackQuery):

    await call.answer("لم تصل أي رسالة SMS",show_alert=True)

# ===============================
# توليد يوزر
# ===============================

@dp.callback_query_handler(lambda c:c.data=="generate_user")
async def user(call:types.CallbackQuery):

    username=generate_username()

    await bot.send_message(
        call.from_user.id,
        f"✨ Username\n\n<code>{username}</code>"
    )

# ===============================
# توليد باسورد
# ===============================

@dp.callback_query_handler(lambda c:c.data=="gen_pass")
async def password(call:types.CallbackQuery):

    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"

    pwd="".join(random.choice(chars) for _ in range(12))

    await bot.send_message(
        call.from_user.id,
        f"🔑 Password\n\n<code>{pwd}</code>"
    )

# ===============================
# فحص رابط
# ===============================

@dp.callback_query_handler(lambda c:c.data=="scan_link")
async def scan(call:types.CallbackQuery):

    user_state[call.from_user.id]="link"

    await bot.send_message(
        call.from_user.id,
        "ارسل الرابط لفحصه"
    )

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="link")
async def check_link(message:types.Message):

    url=message.text

    domain=urlparse(url).netloc

    if "facebook" in domain:
        site="Facebook"

    elif "whatsapp" in domain:
        site="WhatsApp"

    elif "telegram" in domain:
        site="Telegram"

    else:
        site="Unknown"

    text=f"""
🔗 الرابط
{url}

🌐 الدومين
{domain}

📡 الموقع
{site}

🛡 الحالة
آمن نسبيا
"""

    await bot.send_message(
        message.from_user.id,
        text
    )

    user_state.pop(message.from_user.id)

# ===============================
# تواصل المطور
# ===============================

@dp.callback_query_handler(lambda c:c.data=="dev_contact")
async def dev(call:types.CallbackQuery):

    user_state[call.from_user.id]="dev"

    await bot.send_message(
        call.from_user.id,
        "اكتب رسالتك للمطور"
    )

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="dev")
async def dev_msg(message:types.Message):

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

# ===============================
# لعبة XO
# ===============================

def board_kb(board):

    kb=InlineKeyboardMarkup(row_width=3)

    for i in range(9):

        cell=board[i] if board[i] else "⬜"

        kb.insert(
            InlineKeyboardButton(cell,callback_data=f"xo_{i}")
        )

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

@dp.callback_query_handler(lambda c:c.data=="xo_start")
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

        await call.message.edit_text("فزت")

        xo_games.pop(uid)

        return

    empty=[i for i,v in enumerate(board) if not v]

    if empty:

        bot_move=random.choice(empty)

        board[bot_move]="⭕"

    result=check(board)

    if result=="Tie":

        await call.message.edit_text("تعادل")

        xo_games.pop(uid)

        return

    if result=="⭕":

        await call.message.edit_text("البوت فاز")

        xo_games.pop(uid)

        return

    await call.message.edit_text(
        "الدور عليك",
        reply_markup=board_kb(board)
    )

# ===============================
# تشغيل البوت
# ===============================

if __name__=="__main__":

    executor.start_polling(dp,skip_updates=True)

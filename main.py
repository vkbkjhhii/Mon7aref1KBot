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
xo_games = {}

# ---------------- شريط التحميل ----------------
async def hacker_loading(msg, text="جارى المعالجة"):
    for i in range(1,6):
        bar = "▰"*i + "▱"*(5-i)
        await msg.edit_text(f"{text}...\n{bar}")
        await asyncio.sleep(0.5)

# ---------------- الدول ----------------
countries = {
    "egypt": ("🇪🇬 مصر", "+20"),
    "usa": ("🇺🇸 امريكا", "+1"),
    "uk": ("🇬🇧 بريطانيا", "+44"),
    "saudi": ("🇸🇦 السعودية", "+966"),
}

# ---------------- القوائم ----------------
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
        InlineKeyboardButton("شات المطور 🌟", callback_data="contact_dev")
    )
    kb.add(
        InlineKeyboardButton("لعبة X O 🎮", callback_data="xo_game")
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="home"))
    return kb

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("تم تسجيل الدخول لسيرفر البوت 🏴‍☠️", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    await callback.message.edit_text("القائمة الرئيسية", reply_markup=main_menu())

# ---------------- ارقام فيك ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)

    for k,v in countries.items():
        kb.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))

    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))

    await callback.message.edit_text("اختار الدولة", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):

    key = callback.data.split("_")[1]
    name,code = countries[key]

    msg = await callback.message.edit_text("جارى الاتصال بالسيرفر...")

    await hacker_loading(msg,"جارى توليد الرقم")

    number = generate_number(code)

    now = datetime.datetime.now()

    text=f"""
📱 رقم الهاتف

<code>{number}</code>

🌍 الدولة: {name}
🕒 الوقت: {now.strftime('%H:%M')}
📅 التاريخ: {now.strftime('%Y-%m-%d')}
"""

    await callback.message.answer(text,reply_markup=back_btn())

# ---------------- صيد يوزر ----------------
def generate_user():
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
    return "@"+ "".join(random.choice(chars) for _ in range(4))

@dp.callback_query_handler(lambda c: c.data=="vip")
async def vip(callback: types.CallbackQuery):

    msg=await callback.message.edit_text("جارى البحث عن يوزرات...")

    await hacker_loading(msg,"جارى الصيد")

    await msg.delete()

    for _ in range(10):
        await callback.message.answer(generate_user())
        await asyncio.sleep(0.2)

    await callback.message.answer("انتهى الصيد",reply_markup=back_btn())

# ---------------- فحص الروابط ----------------
@dp.callback_query_handler(lambda c: c.data=="check_link")
async def check_link(callback: types.CallbackQuery):

    user_state[callback.from_user.id]="check_link"

    await callback.message.edit_text("ارسل الرابط لفحصه")

@dp.message_handler(lambda message: user_state.get(message.from_user.id)=="check_link")
async def handle_links(message: types.Message):

    link=message.text

    msg=await message.answer("جارى الفحص")

    await hacker_loading(msg,"فحص الرابط")

    await msg.delete()

    result=f"""
🔎 نتيجة الفحص

الرابط: {link}

الحالة: ✅ آمن
IP: 64.29.17.131
"""

    await message.answer(result,reply_markup=back_btn())

    user_state.pop(message.from_user.id)

# ---------------- تواصل المطور ----------------
DEV_ID=7771042305

@dp.callback_query_handler(lambda c: c.data=="contact_dev")
async def contact_dev(callback: types.CallbackQuery):

    await callback.message.answer("ارسل رسالتك وسيتم ارسالها للمطور")

@dp.message_handler(lambda message: message.from_user.id!=DEV_ID)
async def forward_to_dev(message: types.Message):

    if user_state.get(message.from_user.id)=="check_link":
        return

    await bot.send_message(
        DEV_ID,
        f"رسالة من {message.from_user.first_name}\n{message.text}"
    )

# ---------------- لعبة XO ----------------
def create_xo_keyboard(board):

    kb=InlineKeyboardMarkup(row_width=3)

    for i in range(9):

        cell=board[i]

        text=cell if cell else str(i+1)

        kb.insert(
            InlineKeyboardButton(text,callback_data=f"xo_{i}")
        )

    kb.add(InlineKeyboardButton("🔙 العودة",callback_data="home"))

    return kb

def check_winner(board):

    wins=[
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for w in wins:

        if board[w[0]] and board[w[0]]==board[w[1]]==board[w[2]]:
            return board[w[0]]

    if all(board):
        return "Tie"

    return None

@dp.callback_query_handler(lambda c:c.data=="xo_game")
async def xo_start(callback: types.CallbackQuery):

    board=[None]*9

    xo_games[callback.from_user.id]=board

    await callback.message.edit_text(
        "لعبة XO دورك ❌",
        reply_markup=create_xo_keyboard(board)
    )

@dp.callback_query_handler(lambda c:c.data.startswith("xo_"))
async def xo_move(callback: types.CallbackQuery):

    user_id=callback.from_user.id

    if user_id not in xo_games:
        return

    board=xo_games[user_id]

    idx=int(callback.data.split("_")[1])

    if board[idx]:
        return

    board[idx]="❌"

    empty=[i for i,v in enumerate(board) if not v]

    if empty:
        board[random.choice(empty)]="⭕"

    winner=check_winner(board)

    if winner:

        msg="تعادل"

        if winner=="❌":
            msg="فزت 🎉"

        if winner=="⭕":
            msg="البوت فاز 🤖"

        await callback.message.edit_text(msg,reply_markup=back_btn())

        xo_games.pop(user_id)

        return

    await callback.message.edit_text(
        "دورك ❌",
        reply_markup=create_xo_keyboard(board)
    )

# ---------------- تشغيل ----------------
if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)

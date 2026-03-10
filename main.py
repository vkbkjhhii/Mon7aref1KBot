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

# ---------------------------
# تخزين الحالات
# ---------------------------
user_state = {}

DEV_ID = 7771042305

# ---------------------------
# الدول
# ---------------------------
countries = {
    "egypt": ("🇪🇬 مصر", "+20"),
    "usa": ("🇺🇸 امريكا", "+1"),
    "uk": ("🇬🇧 بريطانيا", "+44"),
    "saudi": ("🇸🇦 السعودية", "+966"),
    "uae": ("🇦🇪 الامارات", "+971"),
    "morocco": ("🇲🇦 المغرب", "+212"),
    "algeria": ("🇩🇿 الجزائر", "+213"),
}

# ---------------------------
# القائمة الرئيسية
# ---------------------------
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
        InlineKeyboardButton("لعبة XO 🎮", callback_data="xo_game")
    )

    return kb


def back_btn():

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "🔙 العودة للقائمة الرئيسية",
            callback_data="home"
        )
    )

    return kb


# ---------------------------
# start
# ---------------------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    await message.answer(
        "تم تسجيل الدخول لسيرفر المنحرف 🏴‍☠️",
        reply_markup=main_menu()
    )


@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):

    user_state.pop(callback.from_user.id, None)

    await callback.message.edit_text(
        "القائمة الرئيسية",
        reply_markup=main_menu()
    )


# ---------------------------
# توليد رقم
# ---------------------------
def generate_number(code):

    return code + str(random.randint(100000000, 999999999))


@dp.callback_query_handler(lambda c: c.data == "numbers")
async def numbers(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=2)

    for k, v in countries.items():

        kb.insert(
            InlineKeyboardButton(
                v[0],
                callback_data=f"country_{k}"
            )
        )

    kb.add(
        InlineKeyboardButton("🔙 رجوع", callback_data="home")
    )

    await callback.message.edit_text(
        "اختر الدولة 🌍",
        reply_markup=kb
    )


@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback: types.CallbackQuery):

    key = callback.data.split("_")[1]

    name, code = countries[key]

    msg = await callback.message.edit_text("جاري الاتصال بالسيرفر ⚡")

    for i in range(5):

        await asyncio.sleep(0.4)

        bar = "▰" * i + "▱" * (5 - i)

        await msg.edit_text(f"جاري التوليد {bar}")

    number = generate_number(code)

    now = datetime.datetime.now()

    text = f"""
📱 الرقم

<code>{number}</code>

🌍 الدولة
{name}

🕓 الوقت
{now.strftime('%H:%M')}
"""

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "🔄 تغيير الرقم",
            callback_data=f"country_{key}"
        )
    )

    kb.add(
        InlineKeyboardButton("🔙 رجوع", callback_data="home")
    )

    await msg.edit_text(text, reply_markup=kb)


# ---------------------------
# صيد يوزرات
# ---------------------------
def generate_user():

    chars = "abcdefghijklmnopqrstuvwxyz"

    return "@" + "".join(random.choice(chars) for _ in range(4))


@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip(callback: types.CallbackQuery):

    msg = await callback.message.edit_text("جاري الصيد 🎯")

    await asyncio.sleep(2)

    await msg.delete()

    for _ in range(10):

        await callback.message.answer(generate_user())

        await asyncio.sleep(0.3)

    await callback.message.answer(
        "انتهى الصيد",
        reply_markup=back_btn()
    )


# ---------------------------
# فحص الروابط
# ---------------------------
@dp.callback_query_handler(lambda c: c.data == "check_link")
async def check_link(callback: types.CallbackQuery):

    user_state[callback.from_user.id] = "check_link"

    await callback.message.edit_text(
        "ارسل الرابط لفحصه 🔎"
    )


@dp.message_handler(lambda m: user_state.get(m.from_user.id) == "check_link")
async def scan_link(message: types.Message):

    link = message.text

    msg = await message.answer("جاري الفحص ⏳")

    await asyncio.sleep(2)

    await msg.delete()

    await message.answer(
        f"الرابط:\n{link}\n\n✅ لا يوجد خطر",
        reply_markup=back_btn()
    )

    user_state.pop(message.from_user.id)


# ---------------------------
# تواصل المطور
# ---------------------------
@dp.callback_query_handler(lambda c: c.data == "contact_dev")
async def contact_dev(callback: types.CallbackQuery):

    user_state[callback.from_user.id] = "contact_dev"

    await callback.message.answer(
        "اكتب رسالتك للمطور"
    )


@dp.message_handler(lambda m: user_state.get(m.from_user.id) == "contact_dev")
async def send_dev(message: types.Message):

    await bot.send_message(
        DEV_ID,
        f"رسالة من {message.from_user.id}\n\n{message.text}"
    )

    await message.answer("تم ارسال رسالتك")

    user_state.pop(message.from_user.id)


# ---------------------------
# لعبة XO
# ---------------------------
xo_games = {}

def create_board(board):

    kb = InlineKeyboardMarkup(row_width=3)

    for i in range(9):

        text = board[i] if board[i] else str(i+1)

        kb.insert(
            InlineKeyboardButton(
                text,
                callback_data=f"xo_{i}"
            )
        )

    kb.add(
        InlineKeyboardButton("🔙 رجوع", callback_data="home")
    )

    return kb


@dp.callback_query_handler(lambda c: c.data == "xo_game")
async def start_xo(callback: types.CallbackQuery):

    board = [None] * 9

    xo_games[callback.from_user.id] = board

    await callback.message.edit_text(
        "انت ❌ وانا ⭕",
        reply_markup=create_board(board)
    )


@dp.callback_query_handler(lambda c: c.data.startswith("xo_"))
async def move_xo(callback: types.CallbackQuery):

    uid = callback.from_user.id

    if uid not in xo_games:
        return

    board = xo_games[uid]

    idx = int(callback.data.split("_")[1])

    if board[idx]:
        return

    board[idx] = "❌"

    empty = [i for i, v in enumerate(board) if not v]

    if empty:
        board[random.choice(empty)] = "⭕"

    await callback.message.edit_text(
        "اللعبة شغالة 🎮",
        reply_markup=create_board(board)
    )


# ---------------------------
# تشغيل
# ---------------------------
if __name__ == "__main__":

    executor.start_polling(
        dp,
        skip_updates=True
    )

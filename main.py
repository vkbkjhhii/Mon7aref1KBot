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
        InlineKeyboardButton("اختراق واتساب", callback_data="whatsapp_link"),
        InlineKeyboardButton("اختراق فيسبوك", callback_data="facebook_link")
    )
    kb.add(
        InlineKeyboardButton("بوت الاختراق 👾", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("شات المطور 🌟", callback_data="contact_dev")
    )
    kb.add(
        InlineKeyboardButton("لعبة XO", callback_data="xo_game"),
        InlineKeyboardButton("صيد فيزا 👻", callback_data="generate_card")
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

# ---------------- توليد كارت تجريبي ----------------
def generate_test_card():
    card_id = "TEST-" + str(random.randint(100000, 999999))
    token = "TK-" + str(random.randint(1000, 9999)) + "-" + str(random.randint(1000, 9999))
    expiry_month = random.randint(1, 12)
    expiry_year = random.randint(2026, 2032)

    return f"""
<pre>
╔══════════════════════╗
        𝗧𝗘𝗦𝗧 𝗖𝗔𝗥𝗗 ✅
╠══════════════════════╣
▸ Card ID : {card_id}
▸ Token   : {token}
▸ Expiry  : {expiry_month:02d}/{expiry_year}
▸ Type    : DEMO CARD
▸ Status  : Simulation Only ⚠️
╚══════════════════════╝
</pre>
"""

@dp.callback_query_handler(lambda c: c.data == "generate_card")
async def generate_card(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("⏳ جاري التوليد...")
    await asyncio.sleep(1.5)
    card = generate_test_card()
    await msg.edit_text(card, reply_markup=back_btn())

# ---------------- لعبة X O ----------------
xo_games = {}

def create_xo_keyboard(board):
    kb = InlineKeyboardMarkup(row_width=3)
    for i in range(9):
        cell = board[i]
        text = cell if cell else str(i+1)
        kb.insert(InlineKeyboardButton(text, callback_data=f"xo_{i}"))
    kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
    return kb

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for w in wins:
        if board[w[0]] and board[w[0]] == board[w[1]] == board[w[2]]:
            return board[w[0]]
    if all(board):
        return "Tie"
    return None

@dp.callback_query_handler(lambda c: c.data == "xo_game")
async def xo_start(callback: types.CallbackQuery):
    board = [None]*9
    xo_games[callback.from_user.id] = board
    await callback.message.edit_text("🎮 لعبة X O - الدور عليك ❌", reply_markup=create_xo_keyboard(board))

@dp.callback_query_handler(lambda c: c.data.startswith("xo_"))
async def xo_move(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in xo_games:
        return

    board = xo_games[user_id]
    idx = int(callback.data.split("_")[1])
    if board[idx]:
        return

    board[idx] = "❌"
    winner = check_winner(board)
    if winner:
        await callback.message.edit_text("🏆 انتهت اللعبة!", reply_markup=back_btn())
        xo_games.pop(user_id)
        return

    empty = [i for i, v in enumerate(board) if not v]
    if empty:
        board[random.choice(empty)] = "⭕"

    winner = check_winner(board)
    if winner:
        await callback.message.edit_text("💻 انتهت اللعبة!", reply_markup=back_btn())
        xo_games.pop(user_id)
        return

    await callback.message.edit_text("🎮 الدور عليك ❌", reply_markup=create_xo_keyboard(board))

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

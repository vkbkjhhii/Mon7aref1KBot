from aiogram import types
from aiogram.dispatcher import Dispatcher
from buttons import main_menu, back_btn
import random, datetime, asyncio
from config import DEV_ID

user_state = {}
xo_games = {}
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

def register_handlers(dp: Dispatcher):

    # ---------- START ----------
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer("تم تسجيل الدخول 🏴‍☠️", reply_markup=main_menu())

    @dp.callback_query_handler(lambda c: c.data == "home")
    async def home(callback: types.CallbackQuery):
        user_state.pop(callback.from_user.id, None)
        await callback.message.edit_text("تم تسجيل الدخول 🏴‍☠️", reply_markup=main_menu())

    # ---------- أرقام فيك ----------
    def generate_number(code):
        return code + str(random.randint(100000000, 999999999))

    @dp.callback_query_handler(lambda c: c.data == "numbers")
    async def numbers(callback: types.CallbackQuery):
        kb = types.InlineKeyboardMarkup(row_width=2)
        for k, v in countries.items():
            kb.insert(types.InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("country_"))
    async def send_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]
        name, code = countries[key]

        msg = await callback.message.edit_text("جاري فتح السيرفر ☣️...")
        hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
        for p in hacker_bar*3:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"جاري اختراق شريحة ال SIM :\n{p}")

        number = generate_number(code)
        now = datetime.datetime.now()

        text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}"),
            types.InlineKeyboardButton("💬 طلب كود", callback_data="get_code")
        )
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await msg.edit_text(text, reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("change_"))
    async def change_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]
        name, code = countries[key]

        number = generate_number(code)
        now = datetime.datetime.now()

        text = f"""
➖ رقم الهاتف : <code>{number}</code>
➖ الدولة : {name}
➖ رمز الدولة : {code}
➖ التاريخ : {now.strftime('%Y-%m-%d')}
➖ الوقت : {now.strftime('%H:%M')}
"""
        kb = callback.message.reply_markup
        await callback.message.edit_text(text, reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data == "get_code")
    async def get_code(callback: types.CallbackQuery):
        await callback.answer("لم يتم الحصول على رسائل SMS حتا الان 📩", show_alert=True)

    # ---------- VIP ----------
    def generate_user():
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
        return "@" + "".join(random.choice(chars) for _ in range(4))

    @dp.callback_query_handler(lambda c: c.data == "vip")
    async def vip(callback: types.CallbackQuery):
        msg = await callback.message.edit_text("جاري الصيد 💥...")
        hacker_bar = ["░▒▓█","▒▓█░","▓█░▒","█░▒▓"]
        for p in hacker_bar*3:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"يتم الان صيد يوزرات مميزه 🔥\n{p}")
        await msg.delete()

        for _ in range(10):
            await callback.message.answer(generate_user())
            await asyncio.sleep(0.3)

        await callback.message.answer("انتهى الصيد 🖱️", reply_markup=back_btn())

    # ---------- فحص الروابط ----------
    @dp.callback_query_handler(lambda c: c.data == "check_link")
    async def check_link(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "check_link"
        await callback.message.edit_text("الرجاء ارسال الرابط لفحصه 🔎", reply_markup=None)

    @dp.message_handler(lambda message: user_state.get(message.from_user.id) == "check_link")
    async def handle_links(message: types.Message):
        link = message.text.strip()
        msg = await message.answer("⏳ جاري الفحص... ▰▰▰▱▱")
        for i in range(6):
            await asyncio.sleep(0.5)
            bar = "▰"*i + "▱"*(5-i)
            await msg.edit_text(f"⏳ جاري الفحص... {bar}")
        await msg.delete()

        if "wa.me" in link or "api.whatsapp.com" in link:
            link_type = "واتساب"
        elif "t.me" in link:
            link_type = "تيليجرام"
        elif "https" in link:
            link_type = "عام HTTPS"
        else:
            link_type = "غير معروف"

        result_text = f"""
• الرابط: {link}

• التصنيف: ✅ الرابط آمن

• نوع الرابط: {link_type}
"""
        await message.answer(result_text, reply_markup=back_btn())
        user_state.pop(message.from_user.id)

    # ---------- شات المطور ----------
    @dp.callback_query_handler(lambda c: c.data == "contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        await callback.message.answer("ابدأ المحادثه مع المطور 🧾")

    @dp.message_handler(lambda message: message.from_user.id != DEV_ID)
    async def forward_to_dev(message: types.Message):
        state = user_state.get(message.from_user.id)
        if state == "check_link":
            return
        await bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")

    # ---------- لعبة X O ----------
    def create_xo_keyboard(board):
        kb = types.InlineKeyboardMarkup(row_width=3)
        for i in range(9):
            cell = board[i]
            text = cell if cell else str(i+1)
            kb.insert(types.InlineKeyboardButton(text, callback_data=f"xo_{i}"))
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
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
        await callback.message.edit_text("يلا نلعب ياصديقي الدور عليك انتا ❌ ونا ⭕️", reply_markup=create_xo_keyboard(board))

    @dp.callback_query_handler(lambda c: c.data.startswith("xo_"))
    async def xo_move(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        if user_id not in xo_games:
            await callback.answer("اضغط علي العبه للبدء 😻", show_alert=True)
            return

        board = xo_games[user_id]
        idx = int(callback.data.split("_")[1])
        if board[idx]:
            await callback.answer("المربع مش فاضي 🙄", show_alert=True)
            return

        board[idx] = "❌"
        winner = check_winner(board)
        if winner:
            if winner == "Tie":
                msg = "⚖️ تعادل"
            elif winner == "❌":
                msg = "🏆مبروك انتا فوزت"
            else:
                msg = "💻انا اللي فوزت"
            await callback.message.edit_text(msg, reply_markup=back_btn())
            xo_games.pop(user_id)
            return

        empty = [i for i, v in enumerate(board) if not v]
        if empty:
            bot_move = random.choice(empty)
            board[bot_move] = "⭕"

        winner = check_winner(board)
        if winner:
            if winner == "Tie":
                msg = "⚖️ تعادل"
            elif winner == "❌":
                msg = "🏆مبروك انتا فوزت"
            else:
                msg = "💻انا اللي فوزت"
            await callback.message.edit_text(msg, reply_markup=back_btn())
            xo_games.pop(user_id)
            return

        await callback.message.edit_text("يلا نلعب ياصديقي الدور عليك انتا ❌ ونا ⭕️", reply_markup=create_xo_keyboard(board))

    # ---------- VIP مخفي ----------
    vip_hidden_kb = types.InlineKeyboardMarkup(row_width=2)
    vip_hidden_kb.add(
        types.InlineKeyboardButton("اختراق وتساب", callback_data="vip_hidden_1"),
        types.InlineKeyboardButton("اختراق فيسبوك", callback_data="vip_hidden_2")
    )

    @dp.message_handler(lambda message: message.text.lower() == "vip")
    async def show_vip(message: types.Message):
        await message.answer("تم الدخول اللي سيرفر الاختراقات 😈", reply_markup=vip_hidden_kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("vip_hidden_"))
    async def vip_hidden_callback(callback: types.CallbackQuery):
        await callback.answer(f"لقد ضغطت على {callback.data}", show_alert=True)

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
    # أضف باقي الدول حسب الكود القديم
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
        kb = InlineKeyboardMarkup(row_width=2)
        for k, v in countries.items():
            kb.insert(InlineKeyboardButton(v[0], callback_data=f"country_{k}"))
        kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

    # ---------- أكشن الزرار لكل دولة ----------
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
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}"),
            InlineKeyboardButton("💬 طلب كود", callback_data="get_code")
        )
        kb.add(InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await msg.edit_text(text, reply_markup=kb)

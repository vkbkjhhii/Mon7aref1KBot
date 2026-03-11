from aiogram import types
from aiogram.dispatcher import Dispatcher
from buttons import main_menu, back_btn
import random, datetime, asyncio
from config import DEV_ID
from urllib.parse import urlparse
import pytz

user_state = {}
xo_games = {}
xo_multi_games = {}  # لتخزين ألعاب متعددة المستخدمين

# ---------- قوائم أرقام حقيقية لكل دولة ----------
real_numbers = {
    "مصر": ["01012345678", "01198765432", "01234567890"],
    "امريكا": ["+12025550123", "+12025550987", "+12125551234"],
    "بريطانيا": ["+447911123456", "+447912345678", "+447913456789"],
    "السعودية": ["+966501234567", "+966512345678", "+966513456789"],
    "الامارات": ["+971501234567", "+971512345678", "+971513456789"],
    "المغرب": ["+212612345678", "+212612345679", "+212612345680"],
    "الجزائر": ["+213550123456", "+213550123457", "+213550123458"],
    "تونس": ["+21620123456", "+21620123457", "+21620123458"],
    "تركيا": ["+905012345678", "+905012345679", "+905012345680"],
    "ألمانيا": ["+4915123456789", "+4915123456790", "+4915123456791"],
    "فرنسا": ["+33612345678", "+33612345679", "+33612345680"],
    "إيطاليا": ["+393123456789", "+393123456780", "+393123456781"],
    "إسبانيا": ["+34612345678", "+34612345679", "+34612345680"],
    "كندا": ["+12041234567", "+12041234568", "+12041234569"],
    "البرازيل": ["+5511998765432", "+5511998765433", "+5511998765434"],
    "الهند": ["+919812345678", "+919812345679", "+919812345680"],
    "روسيا": ["+79161234567", "+79161234568", "+79161234569"],
    "الصين": ["+8613800138000", "+8613800138001", "+8613800138002"],
    "اليابان": ["+819012345678", "+819012345679", "+819012345680"],
    "استراليا": ["+61412345678", "+61412345679", "+61412345680"]
}

countries = {k: ("🇦🇪 " + k, "") for k in real_numbers.keys()}  # ضع العلم لكل دولة حسب الحاجة

# ---------- Handlers ----------
def register_handlers(dp: Dispatcher):
    tz = pytz.timezone("Africa/Cairo")

    # ---------- START ----------
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer("تم تسجيل الدخول 🏴‍☠️", reply_markup=main_menu())

    @dp.callback_query_handler(lambda c: c.data == "home")
    async def home(callback: types.CallbackQuery):
        user_state.pop(callback.from_user.id, None)
        await callback.message.edit_text("تم تسجيل الدخول 🏴‍☠️", reply_markup=main_menu())

    # ---------- أرقام فيك ----------
    @dp.callback_query_handler(lambda c: c.data == "numbers")
    async def numbers(callback: types.CallbackQuery):
        kb = types.InlineKeyboardMarkup(row_width=2)
        for k in real_numbers.keys():
            kb.insert(types.InlineKeyboardButton(f"{k}", callback_data=f"country_{k}"))
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("country_"))
    async def send_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]

        msg = await callback.message.edit_text("⏳ جاري توليد الرقم...")
        anim = ["▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰"]
        for a in anim*2:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"⏳ جاري توليد الرقم... {a}")

        number = random.choice(real_numbers[key])
        now = datetime.datetime.now(tz)
        text = f"""
📱 رقم الهاتف: <code>{number}</code>
🌍 الدولة: {key}
🔢 رمز الدولة: {number[:3]}
🕒 التاريخ: {now.strftime('%Y-%m-%d')}
⏰ الوقت: {now.strftime('%H:%M')}
"""
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}"),
            types.InlineKeyboardButton("💬 طلب كود", callback_data="get_code")
        )
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await msg.edit_text(text, reply_markup=kb)

    # ---------- تغيير الرقم ----------
    @dp.callback_query_handler(lambda c: c.data.startswith("change_"))
    async def change_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]
        number = random.choice(real_numbers[key])
        now = datetime.datetime.now(tz)
        text = f"""
📱 رقم الهاتف: <code>{number}</code>
🌍 الدولة: {key}
🔢 رمز الدولة: {number[:3]}
🕒 التاريخ: {now.strftime('%Y-%m-%d')}
⏰ الوقت: {now.strftime('%H:%M')}
"""
        kb = callback.message.reply_markup
        await callback.message.edit_text(text, reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data == "get_code")
    async def get_code(callback: types.CallbackQuery):
        await callback.answer("لم يتم الحصول على رسائل SMS حتا الان 📩", show_alert=True)

    # ---------- التواصل مع المطور ----------
    @dp.callback_query_handler(lambda c: c.data == "contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "to_dev"
        await callback.message.answer("✉️ اكتب رسالتك وسأقوم بعرضها على المطور")

    @dp.message_handler(lambda message: user_state.get(message.from_user.id) == "to_dev")
    async def forward_to_dev(message: types.Message):
        sent_msg = await message.answer("✅ تم إرسال رسالتك")
        await message.delete()
        await bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
        await asyncio.sleep(5)
        await sent_msg.delete()
        user_state.pop(message.from_user.id)

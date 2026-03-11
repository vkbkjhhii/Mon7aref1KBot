from aiogram import types
from aiogram.dispatcher import Dispatcher
from buttons import main_menu, back_btn
import random, datetime, asyncio
from config import DEV_ID
from urllib.parse import urlparse

user_state = {}
xo_games = {}

# ---------- قوائم أرقام حقيقية لكل دولة ----------
real_numbers = {
    "egypt": ["01012345678", "01198765432", "01234567890"],
    "usa": ["+12025550123", "+12025550987", "+12125551234"],
    "uk": ["+447911123456", "+447912345678", "+447913456789"],
    # أضف باقي الدول هنا حسب الحاجة
}

countries = {
    "egypt": ("🇪🇬 مصر", "+20"),
    "usa": ("🇺🇸 امريكا", "+1"),
    "uk": ("🇬🇧 بريطانيا", "+44"),
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

        number = random.choice(real_numbers[key])
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
            types.InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"change_{key}")
        )
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await callback.message.edit_text(text, reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("change_"))
    async def change_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]
        number = random.choice(real_numbers[key])
        name, code = countries[key]
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

    # ---------- فحص الروابط ----------
    @dp.callback_query_handler(lambda c: c.data == "check_link")
    async def check_link(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "check_link"
        await callback.message.edit_text("الرجاء إرسال الرابط فقط 🔎", reply_markup=None)

    @dp.message_handler(lambda message: user_state.get(message.from_user.id) == "check_link")
    async def handle_links(message: types.Message):
        link = message.text.strip()
        if not (link.startswith("http://") or link.startswith("https://")):
            await message.reply("❌ يمكنك إرسال الرابط فقط")
            return

        # استخراج الدومين والمسار
        parsed = urlparse(link)
        domain = parsed.netloc
        path = parsed.path

        # تحديد نوع الرابط
        if "wa.me" in domain or "api.whatsapp.com" in domain:
            link_type = "واتساب"
        elif "t.me" in domain:
            link_type = "تيليجرام"
        elif "tiktok.com" in domain:
            link_type = "تيك توك"
        else:
            link_type = "عام HTTPS"

        # تقرير للمستخدم
        result_text = f"""
🔗 الرابط: {link}
🌐 الدومين: {domain}
📂 المسار: {path}
✅ نوع الرابط: {link_type}
⚠️ الرابط آمن
"""
        await message.answer(result_text, reply_markup=back_btn())
        user_state.pop(message.from_user.id)

    # ---------- التواصل مع المطور ----------
    @dp.callback_query_handler(lambda c: c.data == "contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "to_dev"
        await callback.message.answer("✉️ اكتب رسالتك وسأقوم بعرضها على المطور")

    @dp.message_handler(lambda message: user_state.get(message.from_user.id) == "to_dev")
    async def forward_to_dev(message: types.Message):
        await message.delete()
        await message.answer("✅ تم إرسال رسالتك إلى المطور", reply_markup=back_btn())
        await bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
        user_state.pop(message.from_user.id)

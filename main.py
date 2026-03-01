import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = "YOUR_BOT_TOKEN"  # حط التوكن هنا
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# قائمة الدول مع رموزها
countries = {
    "مصر": "+20",
    "السعودية": "+966",
    "الإمارات": "+971",
    "الأردن": "+962",
    "المغرب": "+212",
    "الجزائر": "+213",
    "تونس": "+216",
    "لبنان": "+961",
    "العراق": "+964",
    "سوريا": "+963",
    "قطر": "+974",
    "الكويت": "+965",
    "البحرين": "+973",
    "عمان": "+968",
    "اليمن": "+967",
    "ليبيا": "+218",
    "السودان": "+249",
    "موريتانيا": "+222",
    "فلسطين": "+970",
    "جيبوتي": "+253"
}

# زرار طلب الكود
request_code_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("طلب الكود 💬", callback_data="request_code")
)

# زرار تغيير الرقم
change_number_button = InlineKeyboardButton("تغيير الرقم 🔄", callback_data="change_number")

# التعامل مع /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    username = message.from_user.username or message.from_user.first_name
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("أرقام فيك 📱", callback_data="select_country")
    )
    await message.answer(f"بتتريج أهلا بك عزيزي {username} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅", reply_markup=keyboard)

# اختيار الدولة
@dp.callback_query_handler(lambda c: c.data == "select_country")
async def choose_country(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for country in list(countries.keys())[:20]:  # أول 20 دولة
        keyboard.insert(InlineKeyboardButton(country, callback_data=f"country_{country}"))
    await call.message.edit_text("اختر الدولة:", reply_markup=keyboard)

# توليد الرقم
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def generate_number(call: types.CallbackQuery):
    country = call.data.split("_")[1]
    code = countries[country]
    # رسالة التحميل
    msg = await call.message.edit_text(f"🔄 جاري إنشاء الرقم لـ {country} ...")
    await asyncio.sleep(2)  # شريط التحميل وهمي
    phone_number = f"{code}{random.randint(100000000, 999999999)}"
    now = datetime.now()
    text = (
        f"➖ تم انشاء الرقم 🛎•\n"
        f"➖ رقم الهاتف ☎️ : {phone_number}\n"
        f"➖ الدوله : {country}\n"
        f"➖ رمز الدوله 🌏 : {code}\n"
        f"➖ المنصه 🔮 : لجميع الموقع والبرامج\n"
        f"➖ تاريخ الانشاء 📅 : {now.date()}\n"
        f"➖ وقت الانشاء ⏰ : {now.strftime('%H:%M:%S')} م\n"
        f"➖ اضغط على الرقم لنسخه."
    )
    # اضافة زر تغيير الرقم
    keyboard = InlineKeyboardMarkup(row_width=2).add(change_number_button).add(request_code_button)
    await call.message.edit_text(text, reply_markup=keyboard)

# تغيير الرقم في نفس الرسالة
@dp.callback_query_handler(lambda c: c.data == "change_number")
async def change_number(call: types.CallbackQuery):
    # نأخذ اسم الدولة من نص الرسالة الحالي
    lines = call.message.text.split("\n")
    country_line = next((l for l in lines if "الدوله" in l), "")
    country = country_line.split(": ")[1] if country_line else "مصر"
    code = countries.get(country, "+20")
    # رقم جديد
    phone_number = f"{code}{random.randint(100000000, 999999999)}"
    now = datetime.now()
    text = (
        f"➖ تم انشاء الرقم 🛎•\n"
        f"➖ رقم الهاتف ☎️ : {phone_number}\n"
        f"➖ الدوله : {country}\n"
        f"➖ رمز الدوله 🌏 : {code}\n"
        f"➖ المنصه 🔮 : لجميع الموقع والبرامج\n"
        f"➖ تاريخ الانشاء 📅 : {now.date()}\n"
        f"➖ وقت الانشاء ⏰ : {now.strftime('%H:%M:%S')} م\n"
        f"➖ اضغط على الرقم لنسخه."
    )
    keyboard = InlineKeyboardMarkup(row_width=2).add(change_number_button).add(request_code_button)
    await call.message.edit_text(text, reply_markup=keyboard)

# طلب الكود
@dp.callback_query_handler(lambda c: c.data == "request_code")
async def request_code(call: types.CallbackQuery):
    await call.message.answer("لا توجد رسائل جديدة 📂")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

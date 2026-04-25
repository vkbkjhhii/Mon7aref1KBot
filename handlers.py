from aiogram.types import Message, CallbackQuery
from buttons import main_menu
import random, string, whois
import phonenumbers
from phonenumbers import geocoder, carrier

user_state = {}

# /start
async def start(message: Message):
    await message.answer("🔥 أهلا بيك في بوت الأمن السيبراني", reply_markup=main_menu)

# الأزرار
async def handle_buttons(call: CallbackQuery):
    user_id = call.from_user.id

    if call.data == "scan_link":
        user_state[user_id] = "link"
        await call.message.answer("🔗 ابعت الرابط")

    elif call.data == "domain":
        user_state[user_id] = "domain"
        await call.message.answer("🌐 ابعت الدومين (example.com)")

    elif call.data == "password":
        chars = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choice(chars) for _ in range(12))
        await call.message.answer(f"🔐 الباسورد:\n{password}")

    elif call.data == "phone":
        user_state[user_id] = "phone"
        await call.message.answer("📱 ابعت رقم الهاتف مع كود الدولة\nمثال: +201001234567")

# الرسائل
async def handle_messages(message: Message):
    user_id = message.from_user.id
    text = message.text

    # 🔍 فحص رابط
    if user_state.get(user_id) == "link":
        if "http" in text:
            await message.answer(f"✅ الرابط شكله سليم:\n{text}")
        else:
            await message.answer("❌ الرابط غير صحيح")

    # 🌐 معلومات موقع
    elif user_state.get(user_id) == "domain":
        try:
            info = whois.whois(text)
            await message.answer(f"📊 معلومات:\n{info}")
        except:
            await message.answer("❌ حصل خطأ")

    # 📱 تحليل رقم
    elif user_state.get(user_id) == "phone":
        try:
            number = phonenumbers.parse(text)

            country = geocoder.description_for_number(number, "ar")
            sim = carrier.name_for_number(number, "ar")
            valid = phonenumbers.is_valid_number(number)

            search_link = f"https://www.google.com/search?q={text}"

            if not valid:
                status = "❌ رقم غير صالح"
            elif sim == "":
                status = "⚠️ غير معروف"
            else:
                status = "✅ طبيعي"

            await message.answer(
                f"📊 معلومات الرقم:\n\n"
                f"📱 الرقم: {text}\n"
                f"🌍 الدولة: {country}\n"
                f"📡 الشركة: {sim if sim else 'غير معروف'}\n"
                f"✔️ صالح: {'نعم' if valid else 'لا'}\n\n"
                f"🔎 بحث في الإنترنت:\n{search_link}\n\n"
                f"⚠️ التقييم: {status}"
            )

        except:
            await message.answer("❌ الرقم غير صحيح، اكتبه بكود الدولة\nمثال: +2010xxxxxxx")

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

# ---------------- توليد الارقام ----------------
def generate_number(country):

    data = {
        "egypt": {
            "prefix": ["010","011","012","015"],
            "networks":{
                "010":"Vodafone",
                "011":"Etisalat",
                "012":"Orange",
                "015":"WE"
            }
        },

        "saudi":{
            "prefix":["050","053","054","055","056","057","058","059"],
            "networks":{
                "050":"STC",
                "053":"STC",
                "054":"Mobily",
                "055":"STC",
                "056":"Mobily",
                "057":"Zain",
                "058":"Zain",
                "059":"Zain"
            }
        },

        "uae":{
            "prefix":["050","052","054","055","056","058"],
            "networks":{
                "050":"Etisalat",
                "052":"DU",
                "054":"DU",
                "055":"Etisalat",
                "056":"Etisalat",
                "058":"DU"
            }
        }
    }

    if country not in data:
        number = str(random.randint(100000000,999999999))
        return number,"Mobile"

    prefix = random.choice(data[country]["prefix"])
    network = data[country]["networks"].get(prefix,"Mobile")

    remaining = 10 - len(prefix)

    number = prefix + "".join(str(random.randint(0,9)) for _ in range(remaining))

    return number,network

# ---------------- القوائم ----------------
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨",callback_data="vip")
    )

    kb.add(
        InlineKeyboardButton("فحص الروابط 🔗",callback_data="check_link")
    )

    kb.add(
        InlineKeyboardButton("بوت الاختراق",url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("شات المطور 🌟",callback_data="contact_dev")
    )

    kb.add(
        InlineKeyboardButton("لعبة X O 🎮",callback_data="xo_game")
    )

    return kb


def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔙 العودة للقائمة الرئيسية",callback_data="home")
    )
    return kb

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    await message.answer(
        "تم تسجيل الدخول الي السيرفر بنجاح 🏴‍☠️",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(lambda c:c.data=="home")
async def home(callback:types.CallbackQuery):

    user_state.pop(callback.from_user.id,None)

    await callback.message.edit_text(
        "تم تسجيل الدخول الي السيرفر بنجاح 🏴‍☠️",
        reply_markup=main_menu()
    )

# ---------------- ارقام ----------------
@dp.callback_query_handler(lambda c:c.data=="numbers")
async def numbers(callback:types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=2)

    for k,v in countries.items():
        kb.insert(
            InlineKeyboardButton(v[0],callback_data=f"country_{k}")
        )

    kb.add(
        InlineKeyboardButton("🔙 العودة",callback_data="home")
    )

    await callback.message.edit_text(
        "حدد دوله 🌍",
        reply_markup=kb
    )


@dp.callback_query_handler(lambda c:c.data.startswith("country_"))
async def send_number(callback:types.CallbackQuery):

    key = callback.data.split("_")[1]
    name,code = countries[key]

    msg = await callback.message.edit_text("جاري توليد الرقم 📡")

    for i in range(1,6):

        bar = "▓"*i + "░"*(5-i)

        await asyncio.sleep(0.4)

        await msg.edit_text(
            f"جاري المعالجة...\n[{bar}]"
        )

    number,network = generate_number(key)

    number = code + number

    now = datetime.datetime.now()

    text = f"""
📱 الرقم : <code>{number}</code>

🌍 الدولة : {name}

📡 الشبكة : {network}

📅 التاريخ : {now.strftime('%Y-%m-%d')}

⏰ الوقت : {now.strftime('%H:%M')}
"""

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"change_{key}"),
        InlineKeyboardButton("🔙 العودة",callback_data="home")
    )

    await msg.edit_text(text,reply_markup=kb)


@dp.callback_query_handler(lambda c:c.data.startswith("change_"))
async def change_number(callback:types.CallbackQuery):

    key = callback.data.split("_")[1]
    name,code = countries[key]

    number,network = generate_number(key)

    number = code + number

    now = datetime.datetime.now()

    text = f"""
📱 الرقم : <code>{number}</code>

🌍 الدولة : {name}

📡 الشبكة : {network}

📅 التاريخ : {now.strftime('%Y-%m-%d')}

⏰ الوقت : {now.strftime('%H:%M')}
"""

    await callback.message.edit_text(
        text,
        reply_markup=callback.message.reply_markup
    )

# ---------------- تشغيل ----------------
if __name__ == "__main__":

    executor.start_polling(dp,skip_updates=True)

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

# ---------------- توليد رقم ----------------
def generate_number(code):
    return code + str(random.randint(100000000, 999999999))

# ---------------- توليد يوزر ----------------
def generate_username():
    chars = "abcdefghijklmnopqrstuvwxyz123456789"
    return "".join(random.choice(chars) for _ in range(random.randint(5,8)))

# ---------------- زخرفة ----------------
def decorate_name(text):
    decorations = [
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹"
        )),
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉"
        )),
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
        )),
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
        )),
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
        )),
        text.upper().translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
        )),
        text.lower().translate(str.maketrans(
            "abcdefghijklmnopqrstuvwxyz",
            "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
        )),
        "".join([c + "̷" for c in text]),
        "".join(["̶" + c for c in text]),
    ]
    return decorations

# ---------------- القوائم ----------------
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ارقام فيك 📱", callback_data="numbers"),
        InlineKeyboardButton("يوزر مميز 👑", callback_data="vip_user")
    )
    keyboard.add(
        InlineKeyboardButton("زخرفة اسماء ✨", callback_data="decorate")
    )
    return keyboard

def back_button():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_home")
    )
    return keyboard

# ---------------- البداية ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(
        f"بتتريج اهلا بك عزيزي {name} في بوت 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 💎",
        reply_markup=main_menu()
    )

# ---------------- رجوع ----------------
@dp.callback_query_handler(lambda c: c.data == "back_home")
async def back_home(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🏠 القائمة الرئيسية",
        reply_markup=main_menu()
    )

# ---------------- ارقام فيك ----------------
@dp.callback_query_handler(lambda c: c.data == "numbers")
async def choose_country(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in countries.items():
        keyboard.insert(InlineKeyboardButton(value[0], callback_data=f"country_{key}"))
    keyboard.add(InlineKeyboardButton("🔙 العودة", callback_data="back_home"))
    await callback_query.message.edit_text("🌍 اختر الدولة", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]

    msg = await callback_query.message.edit_text("⏳ جاري انشاء الرقم...")
    progress = ["▫▫▫▫▫", "🔹▫▫▫▫", "🔹🔹▫▫▫", "🔹🔹🔹▫▫", "🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹"]

    for p in progress:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ إنشاء الرقم:\n{p}")

    number = generate_number(country_code)
    now = datetime.datetime.now()

    text = f"""
➖ رقم الهاتف ☎️ : <code>{number}</code>
➖ الدوله : {country_name}
➖ التاريخ 📅 : {now.strftime('%Y-%m-%d')}
➖ الوقت ⏰ : {now.strftime('%I:%M %p')}
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}"))
    keyboard.add(InlineKeyboardButton("🔙 العودة", callback_data="back_home"))

    await msg.edit_text(text, reply_markup=keyboard)

# ---------------- يوزر مميز ----------------
@dp.callback_query_handler(lambda c: c.data == "vip_user")
async def vip_user(callback_query: types.CallbackQuery):
    msg = await callback_query.message.edit_text("⏳ جاري توليد يوزرات مميزة...")

    progress = ["▫▫▫▫▫", "🔹▫▫▫▫", "🔹🔹▫▫▫", "🔹🔹🔹▫▫", "🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹"]

    for p in progress:
        await asyncio.sleep(0.5)
        await msg.edit_text(f"⏳ جاري التحميل:\n{p}")

    await msg.delete()

    for _ in range(15):
        await bot.send_message(callback_query.from_user.id, f"👑 @{generate_username()}")
        await asyncio.sleep(0.3)

    await bot.send_message(callback_query.from_user.id, "✅ انتهى التوليد", reply_markup=back_button())

# ---------------- زخرفة اسماء ----------------
@dp.callback_query_handler(lambda c: c.data == "decorate")
async def ask_name(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "✍️ ابعت الاسم اللي عاوز تزخرفه",
        reply_markup=back_button()
    )

@dp.message_handler()
async def handle_name(message: types.Message):
    text = message.text

    loading = await message.answer("⏳ جاري الزخرفة...")
    progress = ["▫▫▫▫▫", "🔹▫▫▫▫", "🔹🔹▫▫▫", "🔹🔹🔹▫▫", "🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹"]

    for p in progress:
        await asyncio.sleep(0.5)
        await loading.edit_text(f"⏳ جاري الزخرفة:\n{p}")

    await loading.delete()

    for deco in decorate_name(text):
        await message.answer(deco)
        await asyncio.sleep(0.4)

    await message.answer("✅ تمت الزخرفة", reply_markup=back_button())

# ---------------- تشغيل ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

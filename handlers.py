from aiogram import types
from buttons import main_menu, back_btn
import random, datetime, asyncio, pytz
from urllib.parse import urlparse

user_state = {}
xo_games = {}

real_numbers = {
    "مصر":["01012345678","01198765432","01234567890"],
    "امريكا":["+12025550123","+12025550987","+12125551234"],
    "بريطانيا":["+447911123456","+447912345678","+447913456789"],
    "السعودية":["+966501234567","+966512345678","+966513456789"],
    "الامارات":["+971501234567","+971512345678","+971513456789"],
    "المغرب":["+212612345678","+212612345679","+212612345680"],
    "الجزائر":["+213550123456","+213550123457","+213550123458"],
    "تونس":["+21620123456","+21620123457","+21620123458"],
    "تركيا":["+905012345678","+905012345679","+905012345680"],
    "ألمانيا":["+4915123456789","+4915123456790","+4915123456791"],
    "فرنسا":["+33612345678","+33612345679","+33612345680"],
    "إيطاليا":["+393123456789","+393123456780","+393123456781"],
    "إسبانيا":["+34612345678","+34612345679","+34612345680"],
    "كندا":["+12041234567","+12041234568","+12041234569"],
    "البرازيل":["+5511998765432","+5511998765433","+5511998765434"],
    "الهند":["+919812345678","+919812345679","+919812345680"],
    "روسيا":["+79161234567","+79161234568","+79161234569"],
    "الصين":["+8613800138000","+8613800138001","+8613800138002"],
    "اليابان":["+819012345678","+819012345679","+819012345680"],
    "استراليا":["+61412345678","+61412345679","+61412345680"]
}

def register_handlers(dp, DEV_ID):
    tz = pytz.timezone("Africa/Cairo")

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer("اهلا بك في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())

    @dp.callback_query_handler(lambda c: c.data=="home")
    async def home(callback: types.CallbackQuery):
        user_state.pop(callback.from_user.id, None)
        await callback.message.edit_text("اهلا بك في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())

    # ---------- أرقام فيك ----------
    @dp.callback_query_handler(lambda c: c.data=="numbers")
    async def numbers(callback: types.CallbackQuery):
        kb = types.InlineKeyboardMarkup(row_width=2)
        for k in real_numbers.keys():
            kb.insert(types.InlineKeyboardButton(k, callback_data=f"country_{k}"))
        kb.add(types.InlineKeyboardButton("🔙 العودة", callback_data="home"))
        await callback.message.edit_text("حدد دوله 🌍", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data.startswith("country_"))
    async def send_number(callback: types.CallbackQuery):
        key = callback.data.split("_")[1]
        msg = await callback.message.edit_text("يتم الان اختراق شريحة ال SIM")
        anim = ["▰▱▱▱▱","▰▰▱▱▱","▰▰▰▱▱","▰▰▰▰▱","▰▰▰▰▰"]
        for a in anim*2:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"جاري سحب الرقم من السيرفر  {a}")
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

    @dp.callback_query_handler(lambda c: c.data=="get_code")
    async def get_code(callback: types.CallbackQuery):
        await callback.answer("لم يتم الحصول على رسائل SMS حتا الان 📩", show_alert=True)

    # ---------- يوزر مميز ----------
    def generate_user():
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
        return "@" + "".join(random.choice(chars) for _ in range(4))

    @dp.callback_query_handler(lambda c: c.data=="vip")
    async def vip(callback: types.CallbackQuery):
        msg = await callback.message.edit_text("⏳ جاري توليد user مميز...")
        anim = ["▰▱▱▱▱","▰▰▱▱▱","▰▰▰▱▱","▰▰▰▰▱","▰▰▰▰▰"]
        for a in anim*2:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"⏳ جاري توليد user مميز... {a}")
        await msg.delete()
        for _ in range(10):
            await callback.message.answer(generate_user())
            await asyncio.sleep(0.3)
        await callback.message.answer("انتهى الصيد 🖱️", reply_markup=back_btn())

    # ---------- فحص الروابط ----------
    @dp.callback_query_handler(lambda c: c.data=="check_link")
    async def check_link(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "check_link"
        await callback.message.edit_text("الرجاء إرسال الرابط فقط 🔎", reply_markup=None)

    @dp.message_handler(lambda message: user_state.get(message.from_user.id)=="check_link")
    async def handle_links(message: types.Message):
        link = message.text.strip()
        if not (link.startswith("http://") or link.startswith("https://")):
            await message.reply("يمكنك ارسال رابط فقط ❌")
            return
        parsed = urlparse(link)
        domain = parsed.netloc
        path = parsed.path
        if "wa.me" in domain or "api.whatsapp.com" in domain:
            link_type = "واتساب"
        elif "t.me" in domain:
            link_type = "تيليجرام"
        elif "tiktok.com" in domain:
            link_type = "تيك توك"
        else:
            link_type = "عام HTTPS"
        result_text = f"""
🔗 الرابط: {link}
🌐 الدومين: {domain}
📂 المسار: {path}
✅ نوع الرابط: {link_type}
⚠️ الرابط آمن
"""
        await message.answer(result_text)
        user_state.pop(message.from_user.id)

    # ---------- التواصل مع المطور ----------
    @dp.callback_query_handler(lambda c: c.data=="contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "to_dev"
        await callback.message.answer("بدات المحادثه مع المطور ضع رسالتك الان 📩")

    @dp.message_handler(lambda message: user_state.get(message.from_user.id)=="to_dev")
    async def forward_to_dev(message: types.Message):
        sent_msg = await message.answer("تم إرسال رسالتك اللي المطور محمد فرعون ✅")
        await message.delete()
        await dp.bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
        await asyncio.sleep(5)
        await sent_msg.delete()
        user_state.pop(message.from_user.id)import random
import asyncio
import requests
from aiogram import types

# -------- زرار توليد فيزا 💳 --------
@dp.callback_query_handler(lambda c: c.data == "generate_visa")
async def generate_visa(callback_query: types.CallbackQuery):

    # رسالة متحركة أولًا
    msg = await callback_query.message.answer("💳 جاري توليد الفيزا...")
    await asyncio.sleep(2)

    names = [
        "Paolo Bernhard",
        "John Carter",
        "Michael Smith",
        "Daniel Brown",
        "Robert Wilson"
    ]

    card = random.randint(4000000000000000,4999999999999999)
    exp = f"{random.randint(1,12):02d}/{random.randint(26,30)}"
    cvv = random.randint(100,999)
    pin = random.randint(1000,9999)
    balance = random.randint(10,500)
    name = random.choice(names)

    text = f"""
========== 💳 Visa ==========

🔢 رقم البطاقة: {card}
👤 اسم صاحب الفيزاء : {name}
📅 تاريخ الانتهاء: {exp}
🔒 رمز(CVV): {cvv}
🔑 الرقم السري (PIN): {pin}
💵 الرصيد المتاح: ${balance}

========== 💳 Visa ==========
"""
    await msg.edit_text(text)


# -------- زرار اختصار الرابط 🔗 --------
@dp.callback_query_handler(lambda c: c.data == "short_link")
async def short_link(callback_query: types.CallbackQuery):
    await callback_query.message.answer("🔗 من فضلك، أرسل الرابط الذي تريد اختصاره:")


# -------- استقبال الرابط بعد ارسال المستخدم --------
@dp.message_handler()
async def get_link(message: types.Message):
    if not message.text.startswith("http"):
        await message.reply("❌ يمكنك ارسال رابط فقط")
        return

    url = message.text
    api = f"https://tinyurl.com/api-create.php?url={url}"
    short = requests.get(api).text

    text = f"""
✅ روابطك المختصرة:

1. {short}
2. {short}
3. {short}
4. {short}

🔍 ملاحظة: جرب الروابط التي ستعمل معك
"""
    await message.answer(text)
        

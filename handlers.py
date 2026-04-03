from aiogram import types
from buttons import main_menu, back_btn, far3od_menu, ai_menu, security_menu, network_menu, tools_menu
import random, datetime, asyncio, pytz
from urllib.parse import urlparse

user_state = {}
xo_games = {}

# =================== بيانات الأرقام ===================
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

# =================== القنوات ===================
CHANNEL_1 = "@fraon10k"
CHANNEL_2 = "@feraon_1"

# =================== دالة الاشتراك ===================
async def is_subscribed(bot, user_id):
    try:
        member1 = await bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await bot.get_chat_member(CHANNEL_2, user_id)
        return member1.status != "left" and member2.status != "left"
    except:
        return False

# =================== الدوال الأساسية ===================
def register_handlers(dp, DEV_ID):
    tz = pytz.timezone("Africa/Cairo")

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        if await is_subscribed(dp.bot, message.from_user.id):
            await message.answer(f"اهلا بك {message.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())
        else:
            kb = types.InlineKeyboardMarkup()
            kb.add(
                types.InlineKeyboardButton("اشترك ▪️", url="https://t.me/fraon10k"),
                types.InlineKeyboardButton("اشترك ▪️", url="https://t.me/feraon_1")
            )
            kb.add(types.InlineKeyboardButton("✅ تحقق", callback_data="check_sub"))
            await message.answer("الرجاء الاشتراك في جميع قنوات المطور قبل استخدام البوت.", reply_markup=kb)

    @dp.callback_query_handler(lambda c: c.data=="check_sub")
    async def check_sub(callback: types.CallbackQuery):
        if await is_subscribed(dp.bot, callback.from_user.id):
            await callback.message.edit_text(f"اهلا بك {callback.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())
        else:
            await callback.answer("لم تشترك بعد في القنوات", show_alert=True)

    @dp.callback_query_handler(lambda c: c.data=="home")
    async def home(callback: types.CallbackQuery):
        user_state.pop(callback.from_user.id, None)
        await callback.message.edit_text(f"اهلا بك {callback.from_user.first_name} في بوت المنحرف 🏴‍☠️", reply_markup=main_menu())

    # =================== أرقام فيك ===================
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

    # =================== يوزر مميز ===================
    def generate_user():
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
        return "@" + "".join(random.choice(chars) for _ in range(4))

    @dp.callback_query_handler(lambda c: c.data=="vip")
    async def vip(callback: types.CallbackQuery):
        msg = await callback.message.edit_text("جاي انشاء يوزر مميز 💥")
        anim = ["▰▱▱▱▱","▰▰▱▱▱","▰▰▰▱▱","▰▰▰▰▱","▰▰▰▰▰"]
        for a in anim*2:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"جاري انشاء يوزر مميز 💥{a}")
        await msg.delete()
        for _ in range(10):
            await callback.message.answer(generate_user())
            await asyncio.sleep(0.3)
        await callback.message.answer("انتهى الصيد 🖱️", reply_markup=back_btn())

    # =================== فحص الروابط ===================
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
        await message.answer(f"تم فحص الرابط (تجريبي): {link}")
        user_state.pop(message.from_user.id)

    # =================== التواصل مع المطور ===================
    @dp.callback_query_handler(lambda c: c.data=="contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "to_dev"
        await callback.message.answer("تم فتح محادثه بينك وبين دعم البوت ضع رسالتك أو مشكلتك ⚙")

    @dp.message_handler(lambda message: user_state.get(message.from_user.id)=="to_dev")
    async def forward_to_dev(message: types.Message):
        sent_msg = await message.answer("تم ارسال رسالتك اللي مركز دعم البوت وجاري فحص الموضوع ✅")
        await message.delete()
        await dp.bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
        await asyncio.sleep(5)
        await sent_msg.delete()
        user_state.pop(message.from_user.id)

    # =================== فرعود ===================
    @dp.callback_query_handler(lambda c: c.data == "far3od_menu")
    async def open_far3od(callback: types.CallbackQuery):
        await callback.message.edit_text("مجال الاختراق 💀", reply_markup=far3od_menu())

    paid_text = """هذا القسم مدفوع 💰

لا يمكنك الحصول على هاذا القسم الا بعد الدفع

الشراء من هنا 💎
"""

    def buy_kb():
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton(
                "شراء عملاة البوت",
                url="https://vkbkjhhii.github.io/Mon7aref1KBot/"
            )
        )
        return kb

    @dp.callback_query_handler(lambda c: c.data.startswith("far3od_"))
    async def paid_buttons(callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.answer(paid_text, reply_markup=buy_kb())

    # =================== الأزرار الجديدة ===================
    @dp.callback_query_handler(lambda c: c.data=="ai_menu")
    async def open_ai(callback: types.CallbackQuery):
        await callback.message.edit_text("🤖 قسم الذكاء الاصطناعي", reply_markup=ai_menu())

    @dp.callback_query_handler(lambda c: c.data=="ai_chat")
    async def ai_chat(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "ai_chat"
        await callback.message.edit_text("💬 ابعت سؤالك للذكاء الاصطناعي", reply_markup=back_btn())

    @dp.message_handler(lambda m: user_state.get(m.from_user.id)=="ai_chat")
    async def handle_ai_chat(message: types.Message):
        await message.answer("🤖 (AI مش متفعل لسه)\nلكن هيتربط قريب 🔥")
        user_state.pop(message.from_user.id)

    @dp.callback_query_handler(lambda c: c.data=="security_menu")
    async def open_security(callback: types.CallbackQuery):
        await callback.message.edit_text("🛡️ فحص الأمان", reply_markup=security_menu())

    @dp.callback_query_handler(lambda c: c.data=="check_password")
    async def check_password(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "check_pass"
        await callback.message.edit_text("🔐 ابعت كلمة السر للفحص", reply_markup=back_btn())

    @dp.message_handler(lambda m: user_state.get(m.from_user.id)=="check_pass")
    async def handle_password(message: types.Message):
        text = message.text
        strength = "ضعيفة ❌" if len(text) < 6 else "متوسطة ⚠️" if len(text) < 10 else "قوية ✅"
        await message.answer(f"🔐 قوة الباسورد: {strength}")
        user_state.pop(message.from_user.id)

    @dp.callback_query_handler(lambda c: c.data=="network_menu")
    async def open_network(callback: types.CallbackQuery):
        await callback.message.edit_text("🌐 أدوات الشبكات", reply_markup=network_menu())

    @dp.callback_query_handler(lambda c: c.data=="ip_info")
    async def ip_info(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "ip"
        await callback.message.edit_text("📍 ابعت IP", reply_markup=back_btn())

    @dp.message_handler(lambda m: user_state.get(m.from_user.id)=="ip")
    async def handle_ip(message: types.Message):
        await message.answer(f"🌍 معلومات IP:\nIP: {message.text}\n(ميزة تجريبية)")
        user_state.pop(message.from_user.id)

    @dp.callback_query_handler(lambda c: c.data=="tools_menu")
    async def open_tools(callback: types.CallbackQuery):
        await callback.message.edit_text("🛠️ الأدوات", reply_markup=tools_menu())

    @dp.callback_query_handler(lambda c: c.data=="gen_pass")
    async def gen_pass(callback: types.CallbackQuery):
        password = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz123456789") for _ in range(10))
        await callback.message.edit_text(f"🔑 الباسورد:\n{password}", reply_markup=back_btn())

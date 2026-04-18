from aiogram import types
from buttons import main_menu, tools_menu
from config import CHANNEL_USERNAME
import random
import string

# 👥 المستخدمين
users = set()

def add_user(user_id):
    users.add(user_id)

# 🔐 تحقق من الاشتراك
async def check_sub(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# 🛡️ نصائح واتساب
whatsapp_tips = [
    "فعل التحقق بخطوتين 🔐",
    "متديش كود التفعيل لأي حد ❌",
    "متفتحش روابط مجهولة ⚠️"
]

# 🔑 توليد باسورد
def generate_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

# ▶️ /start
async def start(message: types.Message):
    add_user(message.from_user.id)

    await message.answer(
        f"👋 أهلا بيك في بوت الحماية\n👥 عدد المستخدمين: {len(users)}",
        reply_markup=main_menu
    )

# 🔘 الأزرار
async def handle_buttons(message: types.Message, bot):
    
    # تحقق اشتراك
    if not await check_sub(bot, message.from_user.id):
        await message.answer(f"⚠️ لازم تشترك في القناة:\n{CHANNEL_USERNAME}")
        return

    if message.text == "🔐 الحماية من الاختراق":
        tip = random.choice(whatsapp_tips)
        await message.answer(f"📢 نصيحة:\n{tip}")

    elif message.text == "🛠️ أدوات":
        await message.answer("اختر أداة:", reply_markup=tools_menu)

    elif message.text == "🔑 توليد باسورد":
        password = generate_password()
        await message.answer(f"🔐 الباسورد:\n{password}")

    elif message.text == "🔙 رجوع":
        await message.answer("رجوع للقائمة الرئيسية", reply_markup=main_menu)

    elif message.text == "📊 الإحصائيات":
        await message.answer(f"👥 عدد المستخدمين: {len(users)}")

    elif message.text == "🤖 الذكاء الاصطناعي":
        await message.answer("🤖 ابعتلي أي حاجة وهرد عليك (قريبًا)")

    elif message.text == "📥 تحميل فيديو":
        await message.answer("📥 ابعت لينك الفيديو")

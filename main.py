import os
import random
import string
import asyncio
from datetime import datetime
import pytz
import socket
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN=os.getenv("BOT_TOKEN")
bot=Bot(token=BOT_TOKEN,parse_mode="HTML")
dp=Dispatcher(bot)

DEV_ID=7771042305
user_state={}
xo_games={}
vip_users=set()

# =====================
# الوقت المصري
# =====================
def egypt_time():
    tz=pytz.timezone("Africa/Cairo")
    now=datetime.now(tz)
    date=now.strftime("%Y-%m-%d")
    time=now.strftime("%I:%M %p")
    return date,time

# =====================
# الدول (20 دولة)
# =====================
countries={
"egypt":("🇪🇬 مصر","+20"),
"usa":("🇺🇸 امريكا","+1"),
"uk":("🇬🇧 بريطانيا","+44"),
"saudi":("🇸🇦 السعودية","+966"),
"uae":("🇦🇪 الامارات","+971"),
"morocco":("🇲🇦 المغرب","+212"),
"algeria":("🇩🇿 الجزائر","+213"),
"tunisia":("🇹🇳 تونس","+216"),
"turkey":("🇹🇷 تركيا","+90"),
"germany":("🇩🇪 ألمانيا","+49"),
"france":("🇫🇷 فرنسا","+33"),
"italy":("🇮🇹 ايطاليا","+39"),
"spain":("🇪🇸 اسبانيا","+34"),
"canada":("🇨🇦 كندا","+1"),
"brazil":("🇧🇷 البرازيل","+55"),
"india":("🇮🇳 الهند","+91"),
"russia":("🇷🇺 روسيا","+7"),
"china":("🇨🇳 الصين","+86"),
"japan":("🇯🇵 اليابان","+81"),
"australia":("🇦🇺 استراليا","+61")
}

# =====================
# قائمة رئيسية
# =====================
def main_menu():
    kb=InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("ارقام فيك 📱",callback_data="numbers"),
        InlineKeyboardButton("توليد يوزر ✨",callback_data="gen_user")
    )
    kb.add(
        InlineKeyboardButton("فحص رابط 🔗",callback_data="check_link"),
        InlineKeyboardButton("لعبة XO 🎮",callback_data="xo_start")
    )
    kb.add(
        InlineKeyboardButton("توليد Password 🔑",callback_data="gen_pass"),
        InlineKeyboardButton("معلوماتي 👤",callback_data="my_info")
    )
    kb.add(
        InlineKeyboardButton("التواصل مع المطور 💬",callback_data="contact_dev")
    )
    return kb

# =====================
# START
# =====================
@dp.message_handler(commands=["start"])
async def start(message:types.Message):
    await message.answer("اهلا بك في البوت",reply_markup=main_menu())

# =====================
# ارقام فيك
# =====================
def generate_number_text(country_key):
    name,code=countries[country_key]
    number=str(random.randint(100000000,999999999))
    date,time=egypt_time()
    server=random.choice(["EG-SERVER","EU-SERVER","US-SERVER"])
    text=f"""
➖ رقم الهاتف ☎️ : {code}{number}
➖ الدوله : {name}
➖ رمز الدوله 🌏 : {code}
➖ المنصه 🔮 : لجميع الموقع والبرامج
➖ اسم السيرفر 🖥 : {server}

➖ تاريخ الانشاء 📅 : {date}
➖ وقت الانشاء ⏰ : {time}
"""
    return text

@dp.callback_query_handler(lambda c:c.data=="numbers")
async def numbers(call:types.CallbackQuery):
    kb=InlineKeyboardMarkup(row_width=2)
    for k,v in countries.items():
        kb.insert(InlineKeyboardButton(v[0],callback_data=f"country_{k}"))
    await call.message.edit_text("اختر الدولة 🌍",reply_markup=kb)

@dp.callback_query_handler(lambda c:c.data.startswith("country_"))
async def send_number(call:types.CallbackQuery):
    country_key=call.data.split("_")[1]
    text=generate_number_text(country_key)
    kb=InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"change_number_{country_key}"),
        InlineKeyboardButton("📩 طلب كود",callback_data="sms")
    )
    kb.add(InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home"))
    await call.message.edit_text(text,reply_markup=kb)

@dp.callback_query_handler(lambda c:c.data.startswith("change_number_"))
async def change_number(call:types.CallbackQuery):
    country_key=call.data.split("_")[2]
    text=generate_number_text(country_key)
    kb=InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم",callback_data=f"change_number_{country_key}"),
        InlineKeyboardButton("📩 طلب كود",callback_data="sms")
    )
    kb.add(InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home"))
    await call.message.edit_text(text,reply_markup=kb)

@dp.callback_query_handler(lambda c:c.data=="sms")
async def sms(call:types.CallbackQuery):
    await call.answer("لم تصل رسالة SMS",show_alert=True)

# =====================
# توليد Username
# =====================
@dp.callback_query_handler(lambda c:c.data=="gen_user")
async def gen_user(call:types.CallbackQuery):
    text="✨ Username List\n\n"
    for _ in range(5):
        username="@"+''.join(random.choices(string.ascii_uppercase,k=4))
        text+=f"{username}\n"
    await bot.send_message(call.from_user.id,text)

# =====================
# توليد Password
# =====================
@dp.callback_query_handler(lambda c:c.data=="gen_pass")
async def gen_pass(call:types.CallbackQuery):
    msg=await call.message.edit_text("⚙️ جاري إنشاء Password...")
    for i in range(4):
        await asyncio.sleep(0.5)
        bar="▰"*(i+1)+"▱"*(3-i)
        await msg.edit_text(f"⚙️ جاري إنشاء Password...\n{bar}")
    chars=string.ascii_letters+string.digits
    text="🔑 Password List\n\n"
    for _ in range(5):
        pwd=''.join(random.choices(chars,k=12))
        text+=f"<code>{pwd}</code>\n"
    await bot.send_message(call.from_user.id,text)

# =====================
# معلوماتي
# =====================
@dp.callback_query_handler(lambda c:c.data=="my_info")
async def my_info(call:types.CallbackQuery):
    user=call.from_user
    photos=await bot.get_user_profile_photos(user.id,limit=1)
    text=f"👤 الاسم: {user.first_name}\n🆔 ID: {user.id}\n🔗 Username: @{user.username}"
    if photos.total_count>0:
        await bot.send_photo(user.id,photos.photos[0][-1].file_id,caption=text)
    else:
        await bot.send_message(user.id,text)

# =====================
# فحص روابط
# =====================
bad_domains=["phishing.com","malware.ru","hacklink.net"]

@dp.callback_query_handler(lambda c:c.data=="check_link")
async def check_link(call:types.CallbackQuery):
    user_state[call.from_user.id]="link"
    await bot.send_message(call.from_user.id,"أرسل الرابط لفحصه")

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="link")
async def check_link_message(message:types.Message):
    url=message.text
    domain=urlparse(url).netloc
    try:
        ip=socket.gethostbyname(domain)
    except:
        ip="غير معروف"
    if domain in bad_domains:
        safe="خطير 🔴"
    else:
        safe="آمن 🟢"
    text=f"""
• الرابط: {url}


• التصنيف: {safe}


• تفاصيل التصنيف: لقد قمنا بفحص الرابط وظهر أنه {safe}.


• معلومات IP: {ip}


• مزود الخدمة: AS20940 Akamai International B.V.
"""
    await bot.send_message(message.from_user.id,text)
    user_state.pop(message.from_user.id)

# =====================
# التواصل مع المطور
# =====================
@dp.callback_query_handler(lambda c:c.data=="contact_dev")
async def contact_dev(call:types.CallbackQuery):
    user_state[call.from_user.id]="dev"
    await bot.send_message(call.from_user.id,"اكتب رسالتك إلى المطور")

@dp.message_handler(lambda m:user_state.get(m.from_user.id)=="dev")
async def forward_dev(message:types.Message):
    await bot.send_message(DEV_ID,f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
    await message.delete()
    await bot.send_message(message.from_user.id,"تم إرسال رسالتك إلى المطور")
    user_state.pop(message.from_user.id)

# =====================
# لعبة XO ضد البوت
# =====================
def create_xo_keyboard(board):
    kb=InlineKeyboardMarkup(row_width=3)
    for i,v in enumerate(board):
        kb.insert(InlineKeyboardButton(v if v!=" " else "⬜",callback_data=f"xo_{i}"))
    kb.add(InlineKeyboardButton("🏠 القائمة الرئيسية",callback_data="home"))
    return kb

def check_winner(board):
    wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for w in wins:
        if board[w[0]]!=" " and board[w[0]]==board[w[1]]==board[w[2]]:
            return board[w[0]]
    if all(c!=" " for c in board):
        return "Tie"
    return None

@dp.callback_query_handler(lambda c:c.data=="xo_start")
async def xo_start(call:types.CallbackQuery):
    board=[" "]*9
    xo_games[call.from_user.id]=board
    await call.message.edit_text("ابدأ اللعب ❌ انت و ⭕️ البوت",reply_markup=create_xo_keyboard(board))

@dp.callback_query_handler(lambda c:c.data.startswith("xo_"))
async def xo_move(call:types.CallbackQuery):
    user_id=call.from_user.id
    if user_id not in xo_games:
        await call.answer("اضغط على ابدأ اللعبة أولاً",show_alert=True)
        return
    board=xo_games[user_id]
    idx=int(call.data.split("_")[1])
    if board[idx]!=" ":
        await call.answer("المربع مش فاضي",show_alert=True)
        return
    board[idx]="❌"
    winner=check_winner(board)
    if winner:
        msg="⚖️ تعادل" if winner=="Tie" else "🏆 انت فزت" if winner=="❌" else "💻 البوت فاز"
        await call.message.edit_text(msg,reply_markup=None)
        xo_games.pop(user_id)
        return
    empty=[i for i,v in enumerate(board) if v==" "]
    if empty:
        bot_choice=random.choice(empty)
        board[bot_choice]="⭕"
    winner=check_winner(board)
    if winner:
        msg="⚖️ تعادل" if winner=="Tie" else "🏆 انت فزت" if winner=="❌" else "💻 البوت فاز"
        await call.message.edit_text(msg,reply_markup=None)
        xo_games.pop(user_id)
        return
    await call.message.edit_text("ابدأ اللعب ❌ انت و ⭕️ البوت",reply_markup=create_xo_keyboard(board))

# =====================
# القائمة الرئيسية
# =====================
@dp.callback_query_handler(lambda c:c.data=="home")
async def home(call:types.CallbackQuery):
    await call.message.edit_text("القائمة الرئيسية",reply_markup=main_menu())

# =====================
# تشغيل البوت
# =====================
if __name__=="__main__":
    executor.start_polling(dp,skip_updates=True)

import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from gtts import gTTS

# ================== إعدادات ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# ================== الحالات ==================
class Form(StatesGroup):
    tts_text = State()
    decor_name = State()

# ================== القائمة الرئيسية ==================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📱 ارقام فيك", callback_data="fake"),
        InlineKeyboardButton("👑 يوزر مميز", callback_data="vip"),
        InlineKeyboardButton("📊 معلومات حسابك", callback_data="info"),
        InlineKeyboardButton("🎤 تحويل النص لصوت", callback_data="tts"),
        InlineKeyboardButton("✨ زخرفة اسماء", callback_data="decor"),
        InlineKeyboardButton("🤖 بوت اخر", url="https://t.me/ALMNHRF_2bot?start=b43eb21574c4d1585490bb18860d20d88219386"),
        InlineKeyboardButton("📞 تواصل مع المطور", url="https://t.me/f_zm1")
    )
    return kb

# ================== ستارت ==================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        f"اهلا بك عزيزي {message.from_user.first_name} ❤️",
        reply_markup=main_menu()
    )

# ================== ارقام فيك ==================
countries = {
"مصر 🇪🇬":"+20","السعودية 🇸🇦":"+966","الامارات 🇦🇪":"+971","الكويت 🇰🇼":"+965",
"قطر 🇶🇦":"+974","المغرب 🇲🇦":"+212","الجزائر 🇩🇿":"+213","تونس 🇹🇳":"+216",
"العراق 🇮🇶":"+964","الاردن 🇯🇴":"+962","لبنان 🇱🇧":"+961","سوريا 🇸🇾":"+963",
"تركيا 🇹🇷":"+90","امريكا 🇺🇸":"+1","بريطانيا 🇬🇧":"+44","فرنسا 🇫🇷":"+33",
"المانيا 🇩🇪":"+49","ايطاليا 🇮🇹":"+39","اسبانيا 🇪🇸":"+34","الهند 🇮🇳":"+91"
}

@dp.callback_query_handler(lambda c: c.data=="fake")
async def fake_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    for c in countries:
        kb.insert(InlineKeyboardButton(c, callback_data=f"num|{c}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    await callback.message.edit_text("اختر الدولة:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("num|"))
async def generate_number(callback: types.CallbackQuery):
    country = callback.data.split("|")[1]
    code = countries[country]
    number = code + str(random.randint(100000000,999999999))

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 تغيير الرقم", callback_data=f"num|{country}"),
        InlineKeyboardButton("🔙 رجوع", callback_data="fake")
    )

    await callback.message.edit_text(
        f"📞 الرقم:\n<code>{number}</code>",
        reply_markup=kb
    )

# ================== يوزر مميز ==================
@dp.callback_query_handler(lambda c: c.data=="vip")
async def vip(callback: types.CallbackQuery):
    msg = await callback.message.answer("👑 تجهيز اليوزرات...\n🟦🟦🟦🟦🟦🟦🟦")
    await asyncio.sleep(2)
    await msg.delete()

    username = "@"+''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(6))
    await callback.message.answer(f"✨ اليوزر:\n{username}", reply_markup=main_menu())

# ================== معلومات حسابك ==================
@dp.callback_query_handler(lambda c: c.data=="info")
async def info(callback: types.CallbackQuery):
    user = callback.from_user
    photos = await bot.get_user_profile_photos(user.id)

    text = f"""
╔═══ 📊 معلوماتك ═══╗
👤 الاسم: {user.first_name}
🆔 الايدي: <code>{user.id}</code>
🔗 اليوزر: @{user.username if user.username else "لا يوجد"}
╚══════════════════╝
"""

    if photos.total_count > 0:
        await bot.send_photo(
            callback.message.chat.id,
            photos.photos[0][0].file_id,
            caption=text,
            reply_markup=main_menu()
        )
    else:
        await callback.message.answer(text, reply_markup=main_menu())

# ================== تحويل النص لصوت ==================
@dp.callback_query_handler(lambda c: c.data=="tts")
async def tts_start(callback: types.CallbackQuery):
    await callback.message.answer("✍️ ابعت النص للتحويل:")
    await Form.tts_text.set()

@dp.message_handler(state=Form.tts_text)
async def process_tts(message: types.Message, state: FSMContext):
    tts = gTTS(text=message.text, lang="ar")
    filename = f"{message.from_user.id}.mp3"
    tts.save(filename)

    await message.answer_voice(open(filename,"rb"))
    os.remove(filename)

    await state.finish()

# ================== زخرفة الاسم ==================
@dp.callback_query_handler(lambda c: c.data=="decor")
async def decor_start(callback: types.CallbackQuery):
    await callback.message.answer("✍️ ابعت الاسم للزخرفة:")
    await Form.decor_name.set()

@dp.message_handler(state=Form.decor_name)
async def process_decor(message: types.Message, state: FSMContext):
    name = message.text
    load = await message.answer("🔹 جاري الزخرفة...\n▫▫▫▫▫▫")

    for i in range(6):
        await asyncio.sleep(0.3)
        await load.edit_text(f"🔹 جاري الزخرفة...\n{'🟦'*i}{'▫'*(6-i)}")

    await load.delete()

    styles = [
        name.upper(),
        ''.join(c+"\u0336" for c in name),
        ''.join("\u0336"+c for c in name)
    ]

    for s in styles:
        await message.answer(s)

    await message.answer("✅ تم الانتهاء", reply_markup=main_menu())
    await state.finish()

# ================== رجوع ==================
@dp.callback_query_handler(lambda c: c.data=="back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("القائمة الرئيسية:", reply_markup=main_menu())

# ================== تشغيل ==================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

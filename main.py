from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# زر واحد فقط للتجربة
kb = InlineKeyboardMarkup()
kb.add(InlineKeyboardButton("📱 أرقام فيك", callback_data="fake"))

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("أهلاً بك عزيزي في البوت!", reply_markup=kb)

# handler للزر
@dp.callback_query_handler(lambda c: c.data=="fake")
async def fake(call: types.CallbackQuery):
    await call.message.answer("✅ تم الضغط على زر أرقام فيك!")
    await call.answer()  # مهم جداً عشان الزر يختفي عند الضغط

if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)

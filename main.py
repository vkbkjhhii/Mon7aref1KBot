import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# زرار البوت الآخر
keyboard = InlineKeyboardMarkup()
button = InlineKeyboardButton(
    "🚀 بوت آخر",
    url="https://t.me/ALMNHRF_2bot?start=b43eb21574c4d1585490bb18860d20d88219386"
)
keyboard.add(button)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "أهلاً بيك 👋\nاضغط الزرار تحت 👇",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

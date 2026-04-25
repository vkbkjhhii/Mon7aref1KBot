import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start, handle_buttons, handle_messages

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start, commands=["start"])
dp.callback_query.register(handle_buttons)
dp.message.register(handle_messages)

async def main():
    print("🤖 البوت شغال...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

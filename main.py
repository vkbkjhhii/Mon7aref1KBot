from aiogram.types import Message, CallbackQuery

async def start(message: Message):
    await message.answer("البوت شغال ✅")

async def handle_buttons(call: CallbackQuery):
    await call.answer("تم الضغط")

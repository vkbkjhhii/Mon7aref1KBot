from aiogram import types
from buttons import main_menu

# لينك موقعك (غيره بالرابط بتاعك)
BASE_URL = "https://your-site.onrender.com"

async def start(message: types.Message):
    await message.answer("أهلا بيك 👋", reply_markup=main_menu)


async def handle_buttons(callback: types.CallbackQuery):
    
    if callback.data == "charge":
        await callback.message.answer("اختار الخدمة من الموقع 👇")
        await callback.message.answer(f"{BASE_URL}/index.html")

    elif callback.data == "ai":
        await callback.message.answer("AI Chat 👇")
        await callback.message.answer(f"{BASE_URL}/ai-chat.html")

    elif callback.data == "dark":
        await callback.message.answer("Dark Web Tools 👇")
        await callback.message.answer(f"{BASE_URL}/darkweb.html")

    elif callback.data == "hack":
        await callback.message.answer("Hacker Tools 👇")
        await callback.message.answer(f"{BASE_URL}/hacker.html")

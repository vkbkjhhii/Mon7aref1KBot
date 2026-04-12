from aiogram import types
from buttons import main_menu, back_btn

async def start(message: types.Message):
    await message.answer(
        "🔥 أهلا بيك في البوت",
        reply_markup=main_menu()
    )

async def handle_buttons(call: types.CallbackQuery):

    if call.data == "ai":
        await call.message.edit_text(
            "🤖 AI Chat شغال...",
            reply_markup=back_btn()
        )

    elif call.data == "hacker":
        await call.message.edit_text(
            "💀 Hacker Tools...",
            reply_markup=back_btn()
        )

    elif call.data == "dark":
        await call.message.edit_text(
            "🌐 Dark Web Section...",
            reply_markup=back_btn()
        )

    elif call.data == "back":
        await call.message.edit_text(
            "🔙 رجعنا للقائمة الرئيسية",
            reply_markup=main_menu()
        )

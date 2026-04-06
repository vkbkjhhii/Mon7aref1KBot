from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 شحن", callback_data="charge")],
    [InlineKeyboardButton(text="🤖 AI Chat", callback_data="ai")],
    [InlineKeyboardButton(text="🕶️ Dark Web", callback_data="dark")],
    [InlineKeyboardButton(text="💻 Hacker", callback_data="hack")]
])

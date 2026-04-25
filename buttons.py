from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 فحص رابط", callback_data="scan_link")],
    [InlineKeyboardButton(text="🌐 معلومات موقع", callback_data="domain")],
    [InlineKeyboardButton(text="🔐 توليد باسورد", callback_data="password")],
    [InlineKeyboardButton(text="📱 تحليل رقم", callback_data="phone")]
])

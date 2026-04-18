from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔐 الحماية من الاختراق")],
        [KeyboardButton(text="🤖 الذكاء الاصطناعي")],
        [KeyboardButton(text="🛠️ أدوات")],
        [KeyboardButton(text="📥 تحميل فيديو")],
        [KeyboardButton(text="📊 الإحصائيات")]
    ],
    resize_keyboard=True
)

tools_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎨 زخرفة أسماء")],
        [KeyboardButton(text="🔑 توليد باسورد")],
        [KeyboardButton(text="🔙 رجوع")]
    ],
    resize_keyboard=True
)

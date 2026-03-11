from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# الكيبورد الرئيسي
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    
    # الصف الأول
    kb.add(
        InlineKeyboardButton("ارقام فيك 👽", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )
    
    # الصف الثاني
    kb.add(
        InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link")
    )
    
    # الصف الثالث
    kb.add(
        InlineKeyboardButton("Farm GPT 😈", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("المطور 🥷", callback_data="contact_dev")
    )
    
    # الصف الرابع
    kb.add(
        InlineKeyboardButton("تحت الإصلاح ", callback_data="xo_game")
    )
    
    # ← السطر الجديد للزرار (صف جديد)
    kb.add(
        InlineKeyboardButton("زر جديد 🔥", callback_data="my_new_button")
    )
    kb.add(
    InlineKeyboardButton("زر 1 🔹", callback_data="btn1"),
    InlineKeyboardButton("زر 2 🔹", callback_data="btn2")
    )

    return kb

# زر الرجوع
def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home")
    )
    return kb

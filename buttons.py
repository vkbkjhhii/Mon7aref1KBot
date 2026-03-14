from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# الكيبورد الرئيسي
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("ارقام فيك 👽", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )
    kb.add(
        InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link")
    )
   InlineKeyboardButton("💬 تواصل مع المطور", url="https://vkbkjhhii.github.io/Mon7aref1KBot/") 
    kb.add(
        InlineKeyboardButton("بوت الاختراق", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("المطور 🥷", callback_data="contact_dev")
    )
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home"))
    return kb

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# الكيبورد الرئيسي
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    
    # الصف الأول: 2 زرار كبار
    kb.add(
        InlineKeyboardButton("ارقام فيك 👽", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )
    
    # الصف الثاني: 2 زرار كبار
    kb.add(
        InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link"),
        InlineKeyboardButton("Farm GPT 😈", url="https://t.me/ALMNHRF_Toobot")
    )
    
    # الصف الثالث: 2 زرار كبار
    kb.add(
        InlineKeyboardButton("المطور 🥷", callback_data="contact_dev"),
        InlineKeyboardButton("تحت الإصلاح", callback_data="xo_game")
    )

    kb.add(
    InlineKeyboardButton("توليد فيزا 💳", callback_data="generate_visa"),
    InlineKeyboardButton("اختصار رابط 🔗", callback_data="short_link")
    )
    
    return kb

def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home"))
    return kb

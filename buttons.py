from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# الكيبورد الرئيسي
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    # الصف الأول من الزرار
    kb.add(
        InlineKeyboardButton("ارقام فيك ☎️", callback_data="numbers"),
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip")
    )

    # الصف الثاني
    kb.add(
        InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link")
    )

    # الصف الثالث
    kb.add(
        InlineKeyboardButton("BOT 2", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("دعم البوت ⚙️", callback_data="contact_dev")
    )

    # الصف الرابع: زرار التواصل مع المطور + الزرار الجديد GPT 😈
    kb.add(
        InlineKeyboardButton(
            "المطور 🥷",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/")
        ),
        InlineKeyboardButton(
            "Farm GPT",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/darkweb.html")  # الرابط للصفحة المخيفة
        )
    )

    return kb


# زر الرجوع للقائمة الرئيسية
def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home")
    )
    return kb

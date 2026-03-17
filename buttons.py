from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

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

    kb.add(
        InlineKeyboardButton("BOT 2", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("دعم البوت ⚙️", callback_data="contact_dev")
    )

    # سطر الزرار الجديد جنب زرار التواصل مع المطور
    kb.add(
        InlineKeyboardButton(
            "التواصل مع المطور 💻",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/")
        ),
        InlineKeyboardButton(
            "دخول Dark Web 🕵️‍♂️",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/darkweb.html")  # الرابط للصفحة المخيفة
        )
    )

    return kb


def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home")
    )
    return kb

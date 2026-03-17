from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# الكيبورد الرئيسي
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    # الصف الأول
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

    # الصف الرابع
    kb.add(
        InlineKeyboardButton(
            "المطور 🥷",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/")
        ),
        InlineKeyboardButton(
            "Farm GPT",
            web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/darkweb.html")
        )
    )

    # ✅ الصف الجديد (زر فرعود)
    kb.add(
        InlineKeyboardButton("قسم الاختراق", callback_data="far3od_menu")
    )

    return kb


# ✅ قائمة فرعود (9 أزرار)
def far3od_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("زرار 1", callback_data="far3od_1"),
        InlineKeyboardButton("زرار 2", callback_data="far3od_2")
    )

    kb.add(
        InlineKeyboardButton("زرار 3", callback_data="far3od_3"),
        InlineKeyboardButton("زرار 4", callback_data="far3od_4")
    )

    kb.add(
        InlineKeyboardButton("زرار 5", callback_data="far3od_5"),
        InlineKeyboardButton("زرار 6", callback_data="far3od_6")
    )

    kb.add(
        InlineKeyboardButton("زرار 7", callback_data="far3od_7"),
        InlineKeyboardButton("زرار 8", callback_data="far3od_8")
    )

    # زر لوحده تحت
    kb.add(
        InlineKeyboardButton("زرار 9", callback_data="far3od_9")
    )

    # زر رجوع
    kb.add(
        InlineKeyboardButton("رجوع ↩️", callback_data="home")
    )

    return kb


# زر الرجوع
def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home")
    )
    return kb

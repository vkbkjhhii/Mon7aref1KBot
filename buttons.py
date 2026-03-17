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

    # زر قسم الاختراق
    kb.add(
        InlineKeyboardButton("الهجوم علي جهاز 🚸", callback_data="far3od_menu")
    )

    return kb

# ✅ قائمة فرعود (9 أزرار)
def far3od_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("اختراق وتس 💀", callback_data="far3od_1"),
        InlineKeyboardButton("اختراق فيس💀", callback_data="far3od_2")
    )

    kb.add(
        InlineKeyboardButton("كاميرا اماميه 📸", callback_data="far3od_3"),
        InlineKeyboardButton("كاميرا اخفيه 📷", callback_data="far3od_4")
    )

    kb.add(
        InlineKeyboardButton("حقن فيرس 🦠", callback_data="far3od_5"),
        InlineKeyboardButton("فرمته الهاتف📁", callback_data="far3od_6")
    )

    kb.add(
        InlineKeyboardButton("تتبع الهاتف 🗿", callback_data="far3od_7"),
        InlineKeyboardButton("قفل الهاتف 🔒", callback_data="far3od_8")
    )

    # زر لوحده تحت
    kb.add(
        InlineKeyboardButton("اختراق كاملاً 🔞", callback_data="far3od_9")
    )

    # زر رجوع
    kb.add(
        InlineKeyboardButton("العوده 🔘", callback_data="home")
    )

    return kb

# زر الرجوع للقائمة الرئيسية
def back_btn():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home")
    )
    return kb

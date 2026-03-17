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

    # ✅ زر فرعود الجديد
    kb.add(
        InlineKeyboardButton("قسم الاختراق", callback_data="far3od_menu")
    )

    return kb

# ✅ قائمة فرعود (9 أزرار + الزرين الجدد)
def far3od_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("اختراق وتساب", callback_data="far3od_1"),
        InlineKeyboardButton("اختراق فيس", callback_data="far3od_2")
    )

    kb.add(
        InlineKeyboardButton("الكاميرا الاماميه", callback_data="far3od_3"),
        InlineKeyboardButton("الكاميرا الخالفيه", callback_data="far3od_4")
    )

    kb.add(
        InlineKeyboardButton("حقن فيرس", callback_data="far3od_5"),
        InlineKeyboardButton("فرمته الهاتف", callback_data="far3od_6")
    )

    kb.add(
        InlineKeyboardButton("تتبع الهاتف", callback_data="far3od_7"),
        InlineKeyboardButton("قفل الهاتف ", callback_data="far3od_8")
    )

    # زر لوحده تحت
    kb.add(
        InlineKeyboardButton("لاختراق الهاتف كملا ", callback_data="far3od_9")
    )

    # ✅ الزرين الجدد تحت
    kb.add(
        InlineKeyboardButton("اختصار الرابط 🔗", callback_data="short_link"),
        InlineKeyboardButton("صيد فيزا 💳", callback_data="random_visa")
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

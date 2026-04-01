from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======= الكيبورد الرئيسي =======
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)  # كل زر في صف لوحده = كبير

    kb.add(InlineKeyboardButton("ارقام فيك ☎️", callback_data="numbers"))
    kb.add(InlineKeyboardButton("صيد يوزر ✨", callback_data="vip"))
    kb.add(InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link"))
    kb.add(InlineKeyboardButton("BOT 2", url="https://t.me/ALMNHRF_Toobot"))
    kb.add(InlineKeyboardButton("دعم البوت ⚙️", callback_data="contact_dev"))
    kb.add(InlineKeyboardButton(
        "المطور 🥷",
        web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/")
    ))
    kb.add(InlineKeyboardButton(
        "Farm GPT",
        web_app=WebAppInfo(url="https://vkbkjhhii.github.io/Mon7aref1KBot/darkweb.html")
    ))
    kb.add(InlineKeyboardButton("الهجوم علي جهاز 🚸", callback_data="far3od_menu"))

    return kb

# ======= قائمة فرعود (مستوى level) =======
def far3od_menu():
    kb = InlineKeyboardMarkup(row_width=2)  # صفين لكل مستوى → أكبر من row_width=2 القديم

    # الصف الأول
    kb.add(
        InlineKeyboardButton("اختراق وتس 💀", callback_data="far3od_1"),
        InlineKeyboardButton("اختراق فيس💀", callback_data="far3od_2")
    )

    # الصف الثاني
    kb.add(
        InlineKeyboardButton("كاميرا اماميه 📸", callback_data="far3od_3"),
        InlineKeyboardButton("كاميرا اخفيه 📷", callback_data="far3od_4")
    )

    # الصف الثالث
    kb.add(
        InlineKeyboardButton("حقن فيرس 🦠", callback_data="far3od_5"),
        InlineKeyboardButton("فرمته الهاتف📁", callback_data="far3od_6")
    )

    # الصف الرابع
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

# ======= زر الرجوع للقائمة الرئيسية =======
def back_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home"))
    return kb

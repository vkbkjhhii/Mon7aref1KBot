const { Telegraf, session } = require("telegraf")

const bot = new Telegraf(process.env.BOT_TOKEN)

bot.use(session())

// توليد رقم عشوائي
function generateNumber() {
    const prefix = "+33"
    const random = Math.floor(100000000 + Math.random() * 900000000)
    return prefix + random
}

function getTime() {
    const now = new Date()
    return {
        date: now.toLocaleDateString("ar-EG"),
        time: now.toLocaleTimeString("ar-EG")
    }
}

// رسالة البداية
bot.start(async (ctx) => {
    const msg = await ctx.reply("اضغط الزر لطلب رقم 👇", {
        reply_markup: {
            inline_keyboard: [
                [{ text: "📞 طلب رقم", callback_data: "fake_number" }]
            ]
        }
    })

    // نحفظ message_id عشان نعدل نفس الرسالة
    ctx.session.messageId = msg.message_id
})

// إنشاء رقم
bot.action("fake_number", async (ctx) => {

    const number = generateNumber()
    const { date, time } = getTime()

    ctx.session.number = number

    const text = `
🔔 تم الطلب

📞 رقم الهاتف :
${number}

🌍 الدولة : فرنسا 🇫🇷
🔢 رمز الدولة : +33
🪐 المنصة : لجميع الموقع والبرامج

📅 تاريخ الإنشاء : ${date}
⏰ وقت الإنشاء : ${time}

اضغط ع الرقم لنسخه.
`

    await ctx.telegram.editMessageText(
        ctx.chat.id,
        ctx.session.messageId,
        null,
        text,
        {
            reply_markup: {
                inline_keyboard: [
                    [{ text: "🔄 تغيير الرقم", callback_data: "change_number" }],
                    [{ text: "💬 طلب الكود", callback_data: "get_code" }]
                ]
            }
        }
    )

    await ctx.answerCbQuery()
})

// تغيير الرقم
bot.action("change_number", async (ctx) => {

    const number = generateNumber()
    const { date, time } = getTime()

    ctx.session.number = number

    const text = `
🔔 تم الطلب

📞 رقم الهاتف :
${number}

🌍 الدولة : فرنسا 🇫🇷
🔢 رمز الدولة : +33
🪐 المنصة : لجميع الموقع والبرامج

📅 تاريخ الإنشاء : ${date}
⏰ وقت الإنشاء : ${time}

اضغط ع الرقم لنسخه.
`

    await ctx.telegram.editMessageText(
        ctx.chat.id,
        ctx.session.messageId,
        null,
        text,
        {
            reply_markup: {
                inline_keyboard: [
                    [{ text: "🔄 تغيير الرقم", callback_data: "change_number" }],
                    [{ text: "💬 طلب الكود", callback_data: "get_code" }]
                ]
            }
        }
    )

    await ctx.answerCbQuery()
})

// طلب الكود (وهمي)
bot.action("get_code", async (ctx) => {
    await ctx.answerCbQuery("📭 لا توجد رسائل جديدة", { show_alert: true })
})

bot.launch()

console.log("Bot is running...")

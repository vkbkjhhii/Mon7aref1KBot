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

    ctx.editMessageText(text, {
        reply_markup: {
            inline_keyboard: [
                [{ text: "🔄 تغيير الرقم", callback_data: "change_number" }],
                [{ text: "💬 طلب الكود", callback_data: "get_code" }]
            ]
        }
    })
})

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

    ctx.editMessageText(text, {
        reply_markup: {
            inline_keyboard: [
                [{ text: "🔄 تغيير الرقم", callback_data: "change_number" }],
                [{ text: "💬 طلب الكود", callback_data: "get_code" }]
            ]
        }
    })
})

bot.action("get_code", async (ctx) => {
    ctx.answerCbQuery("لا توجد رسائل جديدة 📭", { show_alert: true })
})

const { Telegraf, Markup, session } = require('telegraf')
const axios = require('axios')

const bot = new Telegraf(process.env.BOT_TOKEN)
bot.use(session())

const CHANNEL = process.env.CHANNEL_USERNAME

// تحقق الاشتراك
async function checkSub(ctx) {
    try {
        const member = await ctx.telegram.getChatMember(CHANNEL, ctx.from.id)
        return ["creator", "administrator", "member"].includes(member.status)
    } catch {
        return false
    }
}

// رسالة ستارت
bot.start(async (ctx) => {

    const isSub = await checkSub(ctx)

    if (!isSub) {
        return ctx.reply(
            "❌ لازم تشترك في القناة أولاً",
            Markup.inlineKeyboard([
                [Markup.button.url("🔔 اشترك", `https://t.me/${CHANNEL.replace("@","")}`)],
                [Markup.button.callback("✅ تحقق", "check_sub")]
            ])
        )
    }

    const photos = await ctx.telegram.getUserProfilePhotos(ctx.from.id)
    let photoId = null

    if (photos.total_count > 0) {
        photoId = photos.photos[0][0].file_id
    }

    const caption = `
╔═══「 👤 بياناتك 」═══╗

الاسم :
${ctx.from.first_name}

ID :
${ctx.from.id}

اليوزر :
@${ctx.from.username || "لا يوجد"}

╚════════════════════╝
`

    const keyboard = Markup.inlineKeyboard([
        [Markup.button.callback("✨ يوزرات مميزة", "usernames")],
        [Markup.button.callback("🎨 زخرفة أسماء", "decorate")],
        [Markup.button.callback("🔍 فحص رابط", "scan")],
        [Markup.button.callback("🎙 تحويل نص لصوت", "tts")],
        [Markup.button.callback("😂 نكتة مصرية", "joke")],
        [Markup.button.callback("🎮 لعبة XO", "xo")],
        [Markup.button.callback("🔗 اختصار رابط", "short")],
        [Markup.button.callback("📩 تواصل مع المطور", "owner")]
    ])

    if (photoId) {
        await ctx.replyWithPhoto(photoId, { caption, ...keyboard })
    } else {
        await ctx.reply(caption, keyboard)
    }
})

bot.action("check_sub", async (ctx) => {
    const isSub = await checkSub(ctx)
    if (isSub) {
        ctx.editMessageText("✅ تم التحقق بنجاح\nاكتب /start")
    } else {
        ctx.answerCbQuery("لسه مش مشترك ❌")
    }
})


// يوزرات عشوائية
bot.action("usernames", async (ctx) => {

    function randomUser(len) {
        const chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        let u = ""
        for (let i=0;i<len;i++){
            u += chars[Math.floor(Math.random()*chars.length)]
        }
        return u
    }

    let list = ""
    for (let i=0;i<10;i++){
        list += `@${randomUser(4)}\n`
    }

    ctx.editMessageCaption(`
✨ يوزرات عشوائية:

${list}
`,
    Markup.inlineKeyboard([
        [Markup.button.callback("🔄 تغيير", "usernames")]
    ])
    )
})


// نكتة
const jokes = [
"مرة واحد بلع مسمار… بقى مسمارح 😂",
"مرة مدرس رياضيات خلف ولد سماه سين 😂",
"مرة واحد بخيل مات… كتبوا على قبره تحت الصيانة 😂"
]

bot.action("joke", async (ctx) => {
    const joke = jokes[Math.floor(Math.random()*jokes.length)]

    ctx.editMessageCaption(`
😂 نكتة اليوم:

${joke}
`,
    Markup.inlineKeyboard([
        [Markup.button.callback("🔄 نكتة تانية", "joke")]
    ])
    )
})

bot.launch()

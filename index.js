const TelegramBot = require('node-telegram-bot-api');

const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

const users = {};

bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    const user = msg.from;

    if (!users[user.id]) {
        users[user.id] = {
            firstSeen: new Date().toLocaleString("ar-EG")
        };
    }

    const text = `
╭───「 👤 بياناتك 」───╮

👑 الاسم :
${user.first_name || "لا يوجد"}

🆔 الايدي :
${user.id}

🔗 اليوزر :
${user.username ? "@" + user.username : "لا يوجد"}

╰──────────────╯
`;

    bot.sendMessage(chatId, text, {
        parse_mode: "HTML",
        reply_markup: {
            inline_keyboard: [
                [
                    { text: "👑 يوزرات مميزة", callback_data: "users" },
                    { text: "✨ زخرفة أسماء", callback_data: "zakhrafa" }
                ],
                [
                    { text: "😂 نكت", callback_data: "jokes" },
                    { text: "🎮 لعبة XO", callback_data: "xo" }
                ],
                [
                    { text: "📩 تواصل مع المطور", callback_data: "dev" }
                ]
            ]
        }
    });
});

bot.on("callback_query", (query) => {
    const chatId = query.message.chat.id;
    const messageId = query.message.message_id;

    if (query.data === "jokes") {
        const jokes = [
            "مرة واحد بخيل مات… كتبوا على قبره تحت الصيانة 😂",
            "واحد دخل الامتحان متأخر… قالهم كنت براجع النوم 😴",
            "مرة مدرس رياضيات خلف ولدين… سماهم س وص 😂"
        ];

        const joke = jokes[Math.floor(Math.random() * jokes.length)];

        bot.editMessageText(`😂 ${joke}`, {
            chat_id: chatId,
            message_id: messageId,
            reply_markup: {
                inline_keyboard: [
                    [{ text: "🔄 نكتة أخرى", callback_data: "jokes" }],
                    [{ text: "⬅ رجوع", callback_data: "back" }]
                ]
            }
        });
    }

    if (query.data === "back") {
        bot.editMessageText("رجعناك للقائمة الرئيسية 👇", {
            chat_id: chatId,
            message_id: messageId
        });
    }

    if (query.data === "dev") {
        bot.sendMessage(chatId, "📩 تم فتح خاصية التواصل مع المطور\n\nأرسل رسالتك الآن.");
    }
});

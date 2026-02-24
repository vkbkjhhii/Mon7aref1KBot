const TelegramBot = require('node-telegram-bot-api');

// 🔴 حط التوكن بتاعك بين العلامات دي بدل النجوم
const token = "8768225608:AAHkYYcW-3wIUykW9UIGMh1qug8XtxIPuwY";

const bot = new TelegramBot(token, { polling: true });

// ===============================
// رسالة الترحيب عند /start
// ===============================

bot.onText(/\/start/, async (msg) => {
    const chatId = msg.chat.id;
    const firstName = msg.from.first_name || "مستخدم";
    const userId = msg.from.id;
    const username = msg.from.username ? "@" + msg.from.username : "لا يوجد";
    const time = new Date().toLocaleString("ar-EG");

    const welcomeMessage = `
👋 أهلاً بك في البوت الخاص بنا

👤 الاسم: ${firstName}
🆔 الايدي: ${userId}
🔗 اليوزر: ${username}
⏰ وقت الدخول: ${time}
🤖 اسم البوت: MonZaref1KBot
`;

    bot.sendMessage(chatId, welcomeMessage, {
        reply_markup: {
            inline_keyboard: [
                [{ text: "📱 أرقام فيك", callback_data: "fake_numbers" }],
                [{ text: "✨ زخرفة", callback_data: "decorate" }],
                [{ text: "🎮 ألعاب", callback_data: "games" }],
                [{ text: "👑 يوزر مميز", callback_data: "vip_user" }],
                [{ text: "📞 تواصل مع المطور", url: "https://t.me/f_zm1" }]
            ]
        }
    });
});

// ===============================
// استقبال ضغط الأزرار
// ===============================

bot.on("callback_query", (query) => {
    const chatId = query.message.chat.id;
    const data = query.data;

    if (data === "fake_numbers") {
        bot.sendMessage(chatId, "📱 اختر الدولة (ميزة تحت التطوير)");
    }

    if (data === "decorate") {
        bot.sendMessage(chatId, "✨ اكتب الاسم اللي عايز تزخرفه");
    }

    if (data === "games") {
        bot.sendMessage(chatId, "🎮 قريبًا سيتم إضافة ألعاب XO وألعاب أخرى");
    }

    if (data === "vip_user") {
        bot.sendMessage(chatId, "👑 سيتم توليد 10 يوزرات مميزة قريبًا");
    }

    bot.answerCallbackQuery(query.id);
});

console.log("✅ Bot is running...");

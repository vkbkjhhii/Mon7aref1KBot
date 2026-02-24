const TelegramBot = require('node-telegram-bot-api');

const token = "8768225608:AAHkYYcW-3wIUykW9UIGMh1qug8XtxIPuwY";

const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "أهلاً بيك 👋\nالبوت اشتغل بنجاح 🔥");
});

bot.on('message', (msg) => {
    if (msg.text !== "/start") {
        bot.sendMessage(msg.chat.id, "إنت قولت: " + msg.text);
    }
});

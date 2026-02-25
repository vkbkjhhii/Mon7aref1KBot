const TelegramBot = require('node-telegram-bot-api');

const token = "8768225608:AAHkYYcW-3wIUykW9UIGMh1qug8XtxIPuwY";

const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, "✅ البوت شغال بنجاح!");
});

console.log("Bot started...");

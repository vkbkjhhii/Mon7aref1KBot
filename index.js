const TelegramBot = require('node-telegram-bot-api');

const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;

    bot.sendMessage(chatId, "اضغط الزر لفتح البوت الآخر 👇", {
        reply_markup: {
            inline_keyboard: [
                [
                    {
                        text: "🤖 بوت آخر",
                        url: "https://t.me/ALMNHRF_2bot?start=b43eb21574c4d1585490bb18860d20d88219386"
                    }
                ]
            ]
        }
    });
});

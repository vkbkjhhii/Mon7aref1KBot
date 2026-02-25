import TelegramBot from "node-telegram-bot-api";
import express from "express";
import axios from "axios";

const token = process.env.BOT_TOKEN;
const url = process.env.RAILWAY_STATIC_URL;

const bot = new TelegramBot(token);
const app = express();

app.use(express.json());

bot.setWebHook(`${url}/bot${token}`);

app.post(`/bot${token}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

app.listen(process.env.PORT || 3000);

const userJoinDate = new Map();

const mainKeyboard = {
  reply_markup: {
    inline_keyboard: [
      [{ text: "🎲 يوزرات مميزة", callback_data: "users" }],
      [{ text: "✨ زخرفة اسماء", callback_data: "zakhrafa" }],
      [{ text: "😂 نكته", callback_data: "joke" }],
      [{ text: "🎮 لعبة XO", callback_data: "xo" }],
      [{ text: "📩 تواصل مع المطور", callback_data: "dev" }]
    ]
  }
};

bot.onText(/\/start/, async (msg) => {
  const chatId = msg.chat.id;
  const user = msg.from;

  if (!userJoinDate.has(user.id)) {
    userJoinDate.set(user.id, new Date().toLocaleDateString());
  }

  const text = `
╭━━━〔 👤 بياناتك 〕━━━╮

👤 الاسم:
${user.first_name}

🆔 الايدي:
${user.id}

🔗 اليوزر:
@${user.username || "لا يوجد"}

╰━━━━━━━━━━━━━━╯
`;

  bot.sendMessage(chatId, text, mainKeyboard);
});

bot.on("callback_query", async (query) => {
  const chatId = query.message.chat.id;

  if (query.data === "users") {
    let list = "";
    for (let i = 0; i < 10; i++) {
      list += `@user${Math.floor(Math.random() * 9999)}\n`;
    }
    bot.editMessageText("⭐ يوزرات مميزة:\n\n" + list, {
      chat_id: chatId,
      message_id: query.message.message_id
    });
  }

  if (query.data === "zakhrafa") {
    bot.editMessageText("✍️ أرسل الاسم الذي تريد زخرفته", {
      chat_id: chatId,
      message_id: query.message.message_id
    });
  }

  if (query.data === "joke") {
    const jokes = [
      "مرة واحد بخيل دخل الجنة قالهم فين العروض 😂",
      "واحد اتجوز مدرسة خلفوا فصل 😂",
      "مرة واحد غبي وقع من السلم فضل يدور على السلم 😂"
    ];
    const random = jokes[Math.floor(Math.random() * jokes.length)];

    bot.editMessageText(random, {
      chat_id: chatId,
      message_id: query.message.message_id,
      reply_markup: {
        inline_keyboard: [
          [{ text: "🔄 نكته أخرى", callback_data: "joke" }]
        ]
      }
    });
  }

  if (query.data === "dev") {
    bot.editMessageText(
      "📩 تم فتح خاصية التواصل مع المطور\n\nأرسل رسالتك الآن وسيتم عرضها على المطور 👑",
      {
        chat_id: chatId,
        message_id: query.message.message_id
      }
    );
  }
});

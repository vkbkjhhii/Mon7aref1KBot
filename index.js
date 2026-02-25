require("dotenv").config();
const TelegramBot = require("node-telegram-bot-api");
const OpenAI = require("openai");

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

const openai = new OpenAI({
  apiKey: process.env.OPENAI_KEY,
});

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, "اهلا بيك 👑\nاختار من القائمة 👇", {
    reply_markup: {
      keyboard: [["🤖 ذكاء اصطناعي"]],
      resize_keyboard: true,
    },
  });
});

bot.on("message", async (msg) => {
  if (msg.text === "🤖 ذكاء اصطناعي") {
    bot.sendMessage(msg.chat.id, "🤖 اكتب سؤالك الآن...");
    return;
  }

  if (!msg.text || msg.text.startsWith("/")) return;

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: msg.text }],
    });

    bot.sendMessage(msg.chat.id, response.choices[0].message.content);
  } catch (error) {
    console.log(error);
    bot.sendMessage(msg.chat.id, "❌ حصل خطأ في الذكاء الاصطناعي");
  }
});

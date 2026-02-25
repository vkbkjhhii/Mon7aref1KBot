const TelegramBot = require("node-telegram-bot-api");
const { OpenAI } = require("openai");

// توكن البوت من المتغيرات
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

// مفتاح الذكاء الاصطناعي
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// زرار البداية
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    `👋 أهلاً ${msg.from.first_name}

🤖 اضغط على زر الذكاء الاصطناعي وابدأ اسأل أي سؤال.`,
    {
      reply_markup: {
        keyboard: [
          ["🤖 الذكاء الاصطناعي"],
        ],
        resize_keyboard: true,
      },
    }
  );
});

// لما المستخدم يضغط زر الذكاء
bot.on("message", async (msg) => {
  if (!msg.text) return;

  if (msg.text === "🤖 الذكاء الاصطناعي") {
    return bot.sendMessage(
      msg.chat.id,
      "💬 اكتب سؤالك الآن..."
    );
  }

  // أي رسالة تانية يرد عليها الذكاء
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: "انت مساعد ذكي ترد بالعربي بشكل احترافي",
        },
        {
          role: "user",
          content: msg.text,
        },
      ],
    });

    bot.sendMessage(
      msg.chat.id,
      response.choices[0].message.content
    );
  } catch (err) {
    bot.sendMessage(
      msg.chat.id,
      "❌ حصل خطأ في الاتصال بالذكاء الاصطناعي"
    );
  }
});

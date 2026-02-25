const { Telegraf, Markup } = require('telegraf');
const axios = require('axios');

const bot = new Telegraf(process.env.BOT_TOKEN);

// تخزين المستخدمين اللي دخلوا وضع الذكاء
let aiUsers = new Set();

bot.start((ctx) => {
  ctx.reply(
    '👑 اهلا بيك في البوت\nاختار من القائمة 👇',
    Markup.keyboard([
      ['📱 أرقام فيك', '✨ زخرفة'],
      ['🤖 ذكاء اصطناعي']
    ]).resize()
  );
});

// دخول وضع الذكاء الاصطناعي
bot.hears('🤖 ذكاء اصطناعي', (ctx) => {
  aiUsers.add(ctx.from.id);
  ctx.reply('🤖 اكتب سؤالك الآن...');
});

// استقبال الرسائل للذكاء
bot.on('text', async (ctx) => {

  if (!aiUsers.has(ctx.from.id)) return;

  const userMessage = ctx.message.text;

  try {
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: "انت مساعد ذكي ترد بالعربي." },
          { role: "user", content: userMessage }
        ]
      },
      {
        headers: {
          "Authorization": `Bearer ${process.env.OPENAI_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    const reply = response.data.choices[0].message.content;

    ctx.reply(reply);

  } catch (error) {
    console.log(error.response?.data || error.message);
    ctx.reply("❌ حصل خطأ في الذكاء الاصطناعي");
  }
});

bot.launch();

console.log("Bot is running 🔥");

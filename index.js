const { Telegraf, Markup } = require('telegraf');
const OpenAI = require('openai');

const bot = new Telegraf(process.env.BOT_TOKEN);

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

let sessions = {};

bot.start((ctx) => {
  ctx.reply(
    "اهلا 👑\nاختار من تحت:",
    Markup.keyboard([['🤖 الذكاء الاصطناعي']]).resize()
  );
});

bot.hears('🤖 الذكاء الاصطناعي', (ctx) => {
  const userId = ctx.from.id;

  sessions[userId] = {
    active: true,
    expires: Date.now() + 10 * 60 * 1000,
  };

  ctx.reply("✅ بدأت المحادثة مع الذكاء الاصطناعي.\n⏳ معاك 10 دقايق.");
});

bot.on('text', async (ctx) => {
  const userId = ctx.from.id;

  if (!sessions[userId] || !sessions[userId].active) return;

  if (Date.now() > sessions[userId].expires) {
    sessions[userId].active = false;
    return ctx.reply("⛔ انتهت مدة الـ 10 دقائق.");
  }

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: ctx.message.text }],
    });

    ctx.reply(response.choices[0].message.content);
  } catch (err) {
    console.log(err);
    ctx.reply("❌ حصل خطأ في الذكاء الاصطناعي.");
  }
});

bot.launch();
console.log("Bot is running...");

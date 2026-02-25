const { Telegraf, Markup } = require("telegraf");
const OpenAI = require("openai");

// ===== تأكد من المتغيرات =====
if (!process.env.BOT_TOKEN) {
  console.log("❌ BOT_TOKEN مش موجود في Variables");
  process.exit(1);
}

if (!process.env.OPENAI_API_KEY) {
  console.log("❌ OPENAI_API_KEY مش موجود في Variables");
}

const bot = new Telegraf(process.env.BOT_TOKEN);

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// تخزين جلسات الذكاء
let sessions = {};

bot.start((ctx) => {
  ctx.reply(
    "👑 أهلاً بيك\nاضغط الزر لبدء الذكاء الاصطناعي:",
    Markup.keyboard([["🤖 الذكاء الاصطناعي"]]).resize()
  );
});

bot.hears("🤖 الذكاء الاصطناعي", (ctx) => {
  const userId = ctx.from.id;

  sessions[userId] = {
    active: true,
    expires: Date.now() + 10 * 60 * 1000, // 10 دقايق
  };

  ctx.reply("✅ بدأت المحادثة مع الذكاء الاصطناعي.\n⏳ معاك 10 دقايق.");
});

bot.on("text", async (ctx) => {
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
    ctx.reply("❌ حصل خطأ في الاتصال بالذكاء الاصطناعي.");
  }
});

bot.launch();
console.log("🚀 Bot is running...");

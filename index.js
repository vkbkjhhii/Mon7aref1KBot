const { Telegraf } = require("telegraf");

const bot = new Telegraf(process.env.BOT_TOKEN);

// أمر start
bot.start((ctx) => {
  ctx.reply("أهلاً بيك في بوت المبرمج فرعون 👑\nاكتب /help عشان تشوف الأوامر");
});

// أمر help
bot.command("help", (ctx) => {
  ctx.reply(`
الأوامر المتاحة:

/start - تشغيل البوت
/help - عرض الأوامر
/id - معرفة الايدي بتاعك
  `);
});

// أمر id
bot.command("id", (ctx) => {
  ctx.reply(`الايدي بتاعك هو: ${ctx.from.id}`);
});

// أي رسالة عادية
bot.on("text", (ctx) => {
  ctx.reply("مش فاهمك 🤖 جرب /help");
});

bot.launch();

console.log("Bot is running...");

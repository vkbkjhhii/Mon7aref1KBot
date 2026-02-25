const { Telegraf } = require("telegraf");

// بنجيب التوكن من Environment Variables
const bot = new Telegraf(process.env.BOT_TOKEN);

// أمر /start
bot.start((ctx) => {
  ctx.reply("البوت اشتغل بنجاح 🔥");
});

// أي رسالة
bot.on("text", (ctx) => {
  ctx.reply("استلمت رسالتك 👌");
});

// تشغيل البوت
bot.launch();

console.log("Bot is running...");

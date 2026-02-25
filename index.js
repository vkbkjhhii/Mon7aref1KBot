const { Telegraf } = require("telegraf");

if (!process.env.BOT_TOKEN) {
  console.error("BOT_TOKEN is missing!");
  process.exit(1);
}

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply("البوت اشتغل 🔥"));
bot.launch();

console.log("Bot is running...");

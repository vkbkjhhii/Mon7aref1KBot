import { Telegraf, Markup } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply(
    "اضغط الزر لفتح البوت الآخر 👇",
    Markup.inlineKeyboard([
      Markup.button.url(
        "🤖 بوت آخر",
        "https://t.me/ALMNHRF_2bot?start=b43eb21574c4d1585490bb18860d20d88219386"
      )
    ])
  );
});

bot.launch();

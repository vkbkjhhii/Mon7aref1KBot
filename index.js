const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");
const axios = require("axios");
const { OpenAI } = require("openai");

const bot = new Telegraf(process.env.BOT_TOKEN);

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

let aiSessions = {};

bot.start(async (ctx) => {
  await ctx.reply(
    `👋 أهلاً ${ctx.from.first_name}`,
    Markup.inlineKeyboard([
      [Markup.button.callback("🤖 الذكاء الاصطناعي", "ai_chat")]
    ])
  );
});

/* ===== زر الذكاء ===== */

bot.action("ai_chat", async (ctx) => {
  aiSessions[ctx.from.id] = {
    active: true,
    expires: Date.now() + 10 * 60 * 1000
  };

  await ctx.reply(
    "🤖 بدأت المحادثة مع الذكاء الاصطناعي\n\n⏳ عندك 10 دقائق."
  );
});

/* ===== استقبال الرسائل ===== */

bot.on("text", async (ctx) => {

  if (aiSessions[ctx.from.id]?.active) {

    if (Date.now() > aiSessions[ctx.from.id].expires) {
      aiSessions[ctx.from.id].active = false;
      await ctx.reply("⛔ انتهت الـ 10 دقائق.");
      return;
    }

    try {
      const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: "انت مساعد ذكي ترد بالعربي" },
          { role: "user", content: ctx.message.text }
        ],
      });

      await ctx.reply(response.choices[0].message.content);

    } catch (err) {
      await ctx.reply("❌ حصل خطأ في الاتصال بالذكاء.");
    }

    return;
  }

});

bot.launch();
console.log("Bot is running 🚀");

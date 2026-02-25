const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

// الردود الثابتة
const aiResponses = {
  "مرحبًا": "أهلاً بيك في البوت!",
  "مساعدتي": "أنا هنا عشان أساعدك في أي حاجة، قول لي بس!",
  "ساعة": new Date().toLocaleTimeString(),
  "تاريخ": new Date().toLocaleDateString(),
  "معلومات": "أنا بوت ذكي شغال على الردود الثابتة.",
};

// البداية
bot.start((ctx) => {
  ctx.reply(
    "اهلا بك في البوت. اكتب كلمة أو سؤال، وسأجيبك بما أعرفه.",
    Markup.keyboard([['مرحبًا', 'مساعدتي', 'ساعة', 'تاريخ', 'معلومات']]).resize()
  );
});

// استماع للرسائل
bot.on('text', (ctx) => {
  const userMessage = ctx.message.text;
  if (aiResponses[userMessage]) {
    ctx.reply(aiResponses[userMessage]);
  } else {
    ctx.reply("آسف، مش فاهم السؤال ده. جرب حاجة تانية.");
  }
});

bot.launch();
console.log("🚀 Bot is running...");

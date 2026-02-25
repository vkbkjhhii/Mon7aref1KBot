const { Telegraf, Markup } = require("telegraf");

const bot = new Telegraf(process.env.BOT_TOKEN);

let aiSessions = {};
let userJoinTime = {};
let lastNumberData = {};

/* ================== القائمة الرئيسية ================== */

function mainMenu() {
  return Markup.inlineKeyboard([
    [
      Markup.button.callback("📱 أرقام فيك", "numbers"),
      Markup.button.callback("✨ زخرفة", "decorate")
    ],
    [
      Markup.button.callback("👑 يوزر مميز", "username"),
      Markup.button.callback("🤖 ذكاء اصطناعي", "ai")
    ]
  ]);
}

/* ================== رسالة الدخول الاحترافية ================== */

bot.start(async (ctx) => {
  userJoinTime[ctx.from.id] = new Date().toLocaleString();

  const welcome = `
╔══════════════════╗
║ 👑 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗣𝗥𝗢 𝗕𝗢𝗧 👑
╠══════════════════╣
║ 👤 الاسم : ${ctx.from.first_name}
║ 🆔 الايدي : ${ctx.from.id}
║ 🤖 البوت : ${ctx.botInfo.first_name}
║ ⏳ وقت الدخول :
║ ${userJoinTime[ctx.from.id]}
╚══════════════════╝
`;

  await ctx.reply(welcome, mainMenu());
});

/* ================== أرقام فيك ================== */

const countries = {
  "🇪🇬 مصر": "+2010",
  "🇸🇦 السعودية": "+9665",
  "🇦🇪 الإمارات": "+9715",
  "🇺🇸 أمريكا": "+1",
  "🇬🇧 بريطانيا": "+44",
  "🇫🇷 فرنسا": "+33",
  "🇩🇪 ألمانيا": "+49",
  "🇮🇹 إيطاليا": "+39",
  "🇪🇸 إسبانيا": "+34",
  "🇹🇷 تركيا": "+90",
  "🇧🇷 البرازيل": "+55",
  "🇨🇦 كندا": "+1",
  "🇮🇳 الهند": "+91",
  "🇵🇰 باكستان": "+92",
  "🇲🇦 المغرب": "+212",
  "🇩🇿 الجزائر": "+213",
  "🇹🇳 تونس": "+216",
  "🇯🇴 الأردن": "+962",
  "🇮🇶 العراق": "+964",
  "🇰🇼 الكويت": "+965"
};

bot.action("numbers", async (ctx) => {
  const buttons = Object.keys(countries).map(name =>
    Markup.button.callback(name, "num_" + name)
  );

  const rows = [];
  for (let i = 0; i < buttons.length; i += 2) {
    rows.push([buttons[i], buttons[i + 1]]);
  }

  await ctx.reply("🌍 اختر الدولة:", Markup.inlineKeyboard(rows));
});

bot.action(/num_(.+)/, async (ctx) => {
  const name = ctx.match[1];
  const prefix = countries[name];

  const number = prefix + Math.floor(1000000 + Math.random() * 9000000);

  lastNumberData[ctx.from.id] = { prefix, messageId: ctx.callbackQuery.message.message_id };

  await ctx.editMessageText(
    `📱 الرقم:\n${number}`,
    Markup.inlineKeyboard([
      [
        Markup.button.callback("🔄 تغيير الرقم", "change_number"),
        Markup.button.callback("📩 طلب كود", "get_code")
      ],
      [Markup.button.callback("🔙 رجوع", "back")]
    ])
  );
});

bot.action("change_number", async (ctx) => {
  const data = lastNumberData[ctx.from.id];
  if (!data) return;

  const newNumber = data.prefix + Math.floor(1000000 + Math.random() * 9000000);

  await ctx.editMessageText(
    `📱 الرقم:\n${newNumber}`,
    Markup.inlineKeyboard([
      [
        Markup.button.callback("🔄 تغيير الرقم", "change_number"),
        Markup.button.callback("📩 طلب كود", "get_code")
      ],
      [Markup.button.callback("🔙 رجوع", "back")]
    ])
  );
});

bot.action("get_code", async (ctx) => {
  const code = Math.floor(100000 + Math.random() * 900000);
  await ctx.answerCbQuery("📨 تم توليد الكود");
  await ctx.reply(`🔢 الكود الخاص بك:\n${code}`);
});

/* ================== يوزر مميز ================== */

function generateUser(length) {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return "@" + result;
}

bot.action("username", async (ctx) => {
  let list = "";
  for (let i = 0; i < 15; i++) {
    list += generateUser(4) + "\n";
  }

  await ctx.reply(
    `👑 15 يوزر مميز:\n\n${list}`,
    Markup.inlineKeyboard([
      [Markup.button.callback("🔙 رجوع", "back")]
    ])
  );
});

/* ================== ذكاء اصطناعي احترافي ================== */

bot.action("ai", async (ctx) => {
  aiSessions[ctx.from.id] = Date.now();

  await ctx.reply("🤖 تم تفعيل الذكاء الاصطناعي لمدة 10 دقائق.\nابدأ المحادثة الآن.");

  setTimeout(() => {
    delete aiSessions[ctx.from.id];
    ctx.telegram.sendMessage(ctx.from.id, "⏳ انتهت جلسة الذكاء الاصطناعي.");
  }, 10 * 60 * 1000);
});

bot.on("text", async (ctx) => {
  if (aiSessions[ctx.from.id]) {

    const msg = ctx.message.text.toLowerCase();

    if (msg.includes("hello") || msg.includes("hi"))
      return ctx.reply("Hello 👋 How can I help you today?");

    if (msg.includes("السلام"))
      return ctx.reply("وعليكم السلام ورحمة الله 👋 كيف أساعدك؟");

    if (msg.includes("who are you"))
      return ctx.reply("I am an advanced AI assistant designed to help you.");

    return ctx.reply("🤖 أفهم ما تقوله... أخبرني أكثر لأساعدك بشكل أفضل.");
  }
});

/* ================== رجوع ================== */

bot.action("back", async (ctx) => {
  await ctx.reply("🔙 القائمة الرئيسية", mainMenu());
});

bot.launch();
console.log("🚀 PRO Bot Running");

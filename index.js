const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");

const bot = new Telegraf(process.env.BOT_TOKEN);

let userState = {};
let aiSessions = {};
let lastGeneratedNumber = {};

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

/* ================= القائمة الرئيسية ================= */

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

bot.start(async (ctx) => {
  await ctx.reply("👑 مرحباً بك في النسخة الاحترافية", mainMenu());
});

/* ================= أرقام ================= */

bot.action("numbers", async (ctx) => {
  const buttons = Object.keys(countries).map(name =>
    Markup.button.callback(name, "num_" + name)
  );

  const rows = [];
  for (let i = 0; i < buttons.length; i += 2) {
    rows.push([buttons[i], buttons[i + 1]]);
  }

  rows.push([Markup.button.callback("🔙 رجوع", "back")]);

  await ctx.reply("🌍 اختر الدولة:", Markup.inlineKeyboard(rows));
});

bot.action(/num_(.+)/, async (ctx) => {
  const name = ctx.match[1];
  const prefix = countries[name];

  const number = prefix + Math.floor(1000000 + Math.random() * 9000000);
  lastGeneratedNumber[ctx.from.id] = number;

  await ctx.reply(
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
  const old = lastGeneratedNumber[ctx.from.id];
  if (!old) return;

  const prefix = old.slice(0, old.length - 7);
  const number = prefix + Math.floor(1000000 + Math.random() * 9000000);
  lastGeneratedNumber[ctx.from.id] = number;

  await ctx.reply(`🔄 رقم جديد:\n${number}`);
});

bot.action("get_code", async (ctx) => {
  const code = Math.floor(100000 + Math.random() * 900000);
  await ctx.reply(`📨 الكود:\n${code}`);
});

/* ================= زخرفة ================= */

const decorations = Array.from({ length: 50 }, (_, i) => (name) =>
  `★${name}★\n꧁${name}꧂\n『${name}』\n✿${name}✿\n彡${name}彡`
);

bot.action("decorate", async (ctx) => {
  userState[ctx.from.id] = "decorate";
  await ctx.reply("✨ اكتب الاسم:");
});

/* ================= يوزر مميز ================= */

bot.action("username", async (ctx) => {
  await ctx.reply(
    "👑 اختر النوع:",
    Markup.inlineKeyboard([
      [
        Markup.button.callback("ثلاثي", "user_3"),
        Markup.button.callback("رباعي", "user_4")
      ],
      [Markup.button.callback("🔙 رجوع", "back")]
    ])
  );
});

function generateUser(length) {
  const chars = "abcdefghijklmnopqrstuvwxyz";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return "@" + result;
}

bot.action("user_3", (ctx) => ctx.reply(generateUser(3)));
bot.action("user_4", (ctx) => ctx.reply(generateUser(4)));

/* ================= ذكاء اصطناعي 10 دقائق ================= */

bot.action("ai", async (ctx) => {
  aiSessions[ctx.from.id] = Date.now();

  await ctx.reply("🤖 بدأت المحادثة لمدة 10 دقائق... اكتب أي شيء.");

  setTimeout(() => {
    delete aiSessions[ctx.from.id];
    ctx.telegram.sendMessage(ctx.from.id, "⏳ انتهت جلسة الذكاء الاصطناعي.");
  }, 10 * 60 * 1000);
});

/* ================= رجوع ================= */

bot.action("back", async (ctx) => {
  await ctx.reply("🔙 رجعنا للقائمة الرئيسية", mainMenu());
});

/* ================= استقبال النص ================= */

bot.on("text", async (ctx) => {

  // زخرفة
  if (userState[ctx.from.id] === "decorate") {
    const name = ctx.message.text;
    const styles = decorations
      .map(fn => fn(name))
      .join("\n\n");

    await ctx.reply("✨ الزخارف:\n\n" + styles);
    userState[ctx.from.id] = null;
    return;
  }

  // AI Session
  if (aiSessions[ctx.from.id]) {
    const replies = [
      "فهمت عليك 👌",
      "ممكن توضح أكتر؟",
      "فكرة جميلة 🔥",
      "أنا معاك",
      "تمام"
    ];
    const reply = replies[Math.floor(Math.random() * replies.length)];
    await ctx.reply(reply);
    return;
  }

});

bot.launch();
console.log("🚀 Bot Running");

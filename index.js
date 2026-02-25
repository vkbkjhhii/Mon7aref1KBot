const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");
const axios = require("axios");

// ===== OpenAI Safe Load =====
let OpenAI = null;
let openai = null;

try {
  OpenAI = require("openai").OpenAI;
  if (process.env.OPENAI_API_KEY) {
    openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
    console.log("✅ OpenAI Ready");
  } else {
    console.log("⚠️ OPENAI_API_KEY مش موجود");
  }
} catch (err) {
  console.log("⚠️ مكتبة openai مش متثبتة");
}

// ===== Bot Init =====
const bot = new Telegraf(process.env.BOT_TOKEN);

const USERS_FILE = "./users.json";
const REQUIRED_CHANNEL = "@x_1fn";
const DEVELOPER_ID = 7771042305;

let waitingForLink = {};
let waitingForDecoration = {};
let aiSessions = {};

if (!fs.existsSync(USERS_FILE)) {
  fs.writeFileSync(USERS_FILE, JSON.stringify({}));
}

function saveUser(user) {
  const users = JSON.parse(fs.readFileSync(USERS_FILE));
  if (!users[user.id]) {
    users[user.id] = {
      name: user.first_name,
      username: user.username || "لا يوجد",
      joinedAt: new Date().toISOString()
    };
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
  }
}

function getUser(id) {
  const users = JSON.parse(fs.readFileSync(USERS_FILE));
  return users[id];
}

/* ================= START ================= */

bot.start(async (ctx) => {
  saveUser(ctx.from);
  const userData = getUser(ctx.from.id);

  const caption = `
👑 أهلاً ${ctx.from.first_name}
🆔 ${ctx.from.id}
📅 ${new Date(userData.joinedAt).toLocaleString()}
  `;

  const buttons = Markup.inlineKeyboard([
    [
      Markup.button.callback("📱 أرقام فيك", "fake_numbers"),
      Markup.button.callback("✨ زخرفة", "decorate")
    ],
    [
      Markup.button.callback("🎮 ألعاب", "games"),
      Markup.button.callback("🔗 فحص", "check_link")
    ],
    [
      Markup.button.callback("🤖 الذكاء الاصطناعي", "ai_chat")
    ],
    [
      Markup.button.callback("🔄 اشتراك", "mandatory_subscription"),
      Markup.button.callback("🗣 المطور", "dev")
    ]
  ]);

  await ctx.reply(caption, buttons);
});

/* ================= الذكاء الاصطناعي ================= */

bot.action("ai_chat", async (ctx) => {
  if (!openai) {
    return ctx.reply("❌ الذكاء غير مفعل حالياً.");
  }

  aiSessions[ctx.from.id] = {
    active: true,
    expires: Date.now() + 10 * 60 * 1000
  };

  await ctx.reply("🤖 بدأت المحادثة مع الذكاء الاصطناعي\n⏳ المدة: 10 دقائق");
});

/* ================= أرقام فيك ================= */

bot.action("fake_numbers", async (ctx) => {
  await ctx.reply("📱 رقم عشوائي: 010" + Math.floor(Math.random()*100000000));
});

/* ================= زخرفة ================= */

bot.action("decorate", async (ctx) => {
  waitingForDecoration[ctx.from.id] = true;
  await ctx.reply("✨ اكتب الاسم:");
});

/* ================= فحص الروابط ================= */

bot.action("check_link", async (ctx) => {
  waitingForLink[ctx.from.id] = true;
  await ctx.reply("🔗 أرسل الرابط:");
});

/* ================= الألعاب ================= */

bot.action("games", async (ctx) => {
  await ctx.reply("🎮 رقم عشوائي: " + (Math.floor(Math.random()*10)+1));
});

/* ================= الاشتراك ================= */

bot.action("mandatory_subscription", async (ctx) => {
  try {
    const status = await ctx.telegram.getChatMember(REQUIRED_CHANNEL, ctx.from.id);
    if (["member", "administrator", "creator"].includes(status.status)) {
      ctx.reply("✅ انت مشترك");
    } else {
      ctx.reply("⚠️ اشترك في القناة: " + REQUIRED_CHANNEL);
    }
  } catch {
    ctx.reply("⚠️ ضيف البوت ادمن في القناة");
  }
});

/* ================= المطور ================= */

bot.action("dev", async (ctx) => {
  ctx.reply("📩 تم إرسال طلبك");
  ctx.telegram.sendMessage(
    DEVELOPER_ID,
    `طلب جديد\n${ctx.from.first_name}\n${ctx.from.id}`
  );
});

/* ================= استقبال الرسائل ================= */

bot.on("text", async (ctx) => {

  // ===== AI Session =====
  if (aiSessions[ctx.from.id]?.active) {

    if (Date.now() > aiSessions[ctx.from.id].expires) {
      aiSessions[ctx.from.id].active = false;
      await ctx.reply("⛔ انتهت الـ 10 دقائق.");
      return;
    }

    if (!openai) return;

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
      console.log(err);
      await ctx.reply("❌ خطأ في الاتصال بالذكاء.");
    }

    return;
  }

  // ===== زخرفة =====
  if (waitingForDecoration[ctx.from.id]) {
    const name = ctx.message.text;
    await ctx.reply(`✨ الزخرفة:\n꧁${name}꧂`);
    waitingForDecoration[ctx.from.id] = false;
    return;
  }

  // ===== فحص رابط =====
  if (waitingForLink[ctx.from.id] && ctx.message.text.startsWith("http")) {
    try {
      const response = await axios.head(ctx.message.text);
      await ctx.reply(response.status === 200 ? "✅ الرابط صالح" : "❌ الرابط غير صالح");
    } catch {
      await ctx.reply("❌ فشل الفحص");
    }
    waitingForLink[ctx.from.id] = false;
    return;
  }

});

/* ================= تشغيل ================= */

bot.launch();
console.log("🚀 Bot Running");

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));

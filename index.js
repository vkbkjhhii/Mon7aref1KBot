const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");
const axios = require("axios");

const bot = new Telegraf(process.env.BOT_TOKEN);

const USERS_FILE = "./users.json";
const REQUIRED_CHANNEL = "@x_1fn";
const DEVELOPER_ID = 7771042305;

let waitingForLink = {};

// إنشاء ملف المستخدمين لو مش موجود
if (!fs.existsSync(USERS_FILE)) {
  fs.writeFileSync(USERS_FILE, JSON.stringify({}));
}

// حفظ المستخدم
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

// جلب بيانات مستخدم
function getUser(id) {
  const users = JSON.parse(fs.readFileSync(USERS_FILE));
  return users[id];
}

/* ================= START ================= */

bot.start(async (ctx) => {
  saveUser(ctx.from);
  const userData = getUser(ctx.from.id);

  let photo = null;
  try {
    const profilePhotos = await ctx.telegram.getUserProfilePhotos(ctx.from.id);
    if (profilePhotos.total_count > 0) {
      photo = profilePhotos.photos[0][0].file_id;
    }
  } catch {}

  const caption = `
👤 الاسم: ${ctx.from.first_name}
🆔 الايدي: ${ctx.from.id}
🤖 اسم البوت: ${ctx.botInfo.first_name}
⏱ وقت الدخول: ${new Date(userData.joinedAt).toLocaleString()}
  `;

  const buttons = Markup.inlineKeyboard([
    [Markup.button.callback("📱 أرقام فيك", "fake_numbers")],
    [Markup.button.callback("✨ زخرفة أسماء", "decorate")],
    [Markup.button.callback("🎮 ألعاب", "games")],
    [Markup.button.callback("🧠 ذكاء اصطناعي", "ai")],
    [Markup.button.callback("🔗 فحص الروابط", "check_link")],
    [Markup.button.callback("🔄 الاشتراك الإجباري", "mandatory_subscription")],
    [Markup.button.callback("🗣 المطور", "dev")]
  ]);

  if (photo) {
    await ctx.replyWithPhoto(photo, { caption, ...buttons });
  } else {
    await ctx.reply(caption, buttons);
  }
});

/* ================= فحص الروابط ================= */

bot.action("check_link", async (ctx) => {
  waitingForLink[ctx.from.id] = true;
  await ctx.reply("📝 أرسل الرابط الذي تريد فحصه.");
});

bot.on("text", async (ctx) => {
  if (waitingForLink[ctx.from.id] && ctx.message.text.startsWith("http")) {
    try {
      const response = await axios.head(ctx.message.text);
      if (response.status === 200) {
        await ctx.reply("✅ الرابط صالح.");
      } else {
        await ctx.reply("❌ الرابط غير صالح.");
      }
    } catch (error) {
      await ctx.reply("❌ حدث خطأ أثناء فحص الرابط.");
    }
    waitingForLink[ctx.from.id] = false;
  }
});

/* ================= الاشتراك الإجباري ================= */

bot.action("mandatory_subscription", async (ctx) => {
  try {
    const status = await ctx.telegram.getChatMember(REQUIRED_CHANNEL, ctx.from.id);

    if (["member", "administrator", "creator"].includes(status.status)) {
      await ctx.reply("🌟 تم التأكد من اشتراكك في القناة!");
    } else {
      await ctx.reply(`⚠️ يجب الاشتراك أولاً في القناة:\n${REQUIRED_CHANNEL}`);
    }
  } catch (err) {
    await ctx.reply("⚠️ تأكد أن البوت مضاف كأدمن في القناة.");
  }
});

/* ================= المطور ================= */

bot.action("dev", async (ctx) => {
  await ctx.reply("📩 تم إرسال طلبك إلى المطور.");

  await ctx.telegram.sendMessage(
    DEVELOPER_ID,
    `📲 مستخدم يريد التواصل:
👤 الاسم: ${ctx.from.first_name}
🆔 الايدي: ${ctx.from.id}
@${ctx.from.username || "لا يوجد"}`
  );
});

/* ================= الألعاب ================= */

bot.action("games", async (ctx) => {
  await ctx.reply(
    "🎮 اختر اللعبة:",
    Markup.inlineKeyboard([
      [Markup.button.callback("🎯 التخمين", "game_1")],
      [Markup.button.callback("❓ أسئلة عامة", "game_2")]
    ])
  );
});

bot.action("game_1", async (ctx) => {
  const random = Math.floor(Math.random() * 10) + 1;
  await ctx.reply(`🎯 خمن رقم بين 1 و 10\n(الرقم هو: ${random})`);
});

bot.action("game_2", async (ctx) => {
  await ctx.reply("❓ عاصمة فرنسا؟\n1️⃣ باريس\n2️⃣ روما\n3️⃣ مدريد");
});

/* ================= تشغيل البوت ================= */

bot.launch();
console.log("Bot is running 🚀");

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));

const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");
const axios = require("axios");

const bot = new Telegraf(process.env.BOT_TOKEN);

const USERS_FILE = "./users.json";
const REQUIRED_CHANNEL = "@x_1fn";
const DEVELOPER_ID = 7771042305;

let waitingForLink = {};
let waitingForDecoration = {};

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

  let photo = null;
  try {
    const profilePhotos = await ctx.telegram.getUserProfilePhotos(ctx.from.id);
    if (profilePhotos.total_count > 0) {
      photo = profilePhotos.photos[0][0].file_id;
    }
  } catch {}

  const caption = `
╔═══『 👑 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 👑 』═══╗
┃ 👤 الاسم: ${ctx.from.first_name}
┃ 🆔 الايدي: ${ctx.from.id}
┃ 🤖 البوت: ${ctx.botInfo.first_name}
┃ 📅 وقت الدخول:
┃ ${new Date(userData.joinedAt).toLocaleString()}
╚════════════════════╝
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
      Markup.button.callback("🔄 اشتراك", "mandatory_subscription"),
      Markup.button.callback("🗣 المطور", "dev")
    ]
  ]);

  if (photo) {
    await ctx.replyWithPhoto(photo, { caption, ...buttons });
  } else {
    await ctx.reply(caption, buttons);
  }
});

/* ================= أرقام فيك ================= */

bot.action("fake_numbers", async (ctx) => {
  await ctx.answerCbQuery();

  await ctx.reply(
    "🌍 اختر الدولة:",
    Markup.inlineKeyboard([
      [
        Markup.button.callback("🇪🇬 مصر", "num_eg"),
        Markup.button.callback("🇸🇦 السعودية", "num_sa")
      ],
      [
        Markup.button.callback("🇺🇸 أمريكا", "num_us"),
        Markup.button.callback("🇦🇪 الإمارات", "num_ae")
      ]
    ])
  );
});

function randomNumber(prefix, length) {
  return prefix + Math.floor(Math.random() * Math.pow(10, length)).toString().padStart(length, "0");
}

bot.action("num_eg", (ctx) => ctx.reply("📱 " + randomNumber("010", 8)));
bot.action("num_sa", (ctx) => ctx.reply("📱 " + randomNumber("05", 8)));
bot.action("num_us", (ctx) => ctx.reply("📱 " + randomNumber("+1", 9)));
bot.action("num_ae", (ctx) => ctx.reply("📱 " + randomNumber("050", 7)));

/* ================= زخرفة ================= */

bot.action("decorate", async (ctx) => {
  waitingForDecoration[ctx.from.id] = true;
  await ctx.reply("✨ اكتب الاسم اللي عايز تزخرفه:");
});

/* ================= فحص الروابط ================= */

bot.action("check_link", async (ctx) => {
  waitingForLink[ctx.from.id] = true;
  await ctx.reply("🔗 أرسل الرابط:");
});

/* ================= الألعاب ================= */

bot.action("games", async (ctx) => {
  await ctx.reply(
    "🎮 اختر لعبة:",
    Markup.inlineKeyboard([
      [
        Markup.button.callback("🎯 تخمين", "game1"),
        Markup.button.callback("❓ سؤال", "game2")
      ]
    ])
  );
});

bot.action("game1", (ctx) => {
  const num = Math.floor(Math.random() * 10) + 1;
  ctx.reply(`🎯 الرقم هو: ${num}`);
});

bot.action("game2", (ctx) => {
  ctx.reply("❓ عاصمة مصر؟\n1️⃣ القاهرة\n2️⃣ دبي\n3️⃣ الرياض");
});

/* ================= الاشتراك ================= */

bot.action("mandatory_subscription", async (ctx) => {
  try {
    const status = await ctx.telegram.getChatMember(REQUIRED_CHANNEL, ctx.from.id);
    if (["member", "administrator", "creator"].includes(status.status)) {
      ctx.reply("✅ انت مشترك بالفعل!");
    } else {
      ctx.reply("⚠️ لازم تشترك في القناة: " + REQUIRED_CHANNEL);
    }
  } catch {
    ctx.reply("⚠️ ضيف البوت ادمن في القناة.");
  }
});

/* ================= المطور ================= */

bot.action("dev", async (ctx) => {
  ctx.reply("📩 تم إرسال طلبك للمطور.");
  ctx.telegram.sendMessage(
    DEVELOPER_ID,
    `📢 طلب تواصل جديد
👤 ${ctx.from.first_name}
🆔 ${ctx.from.id}
@${ctx.from.username || "لا يوجد"}`
  );
});

/* ================= استقبال الرسائل ================= */

bot.on("text", async (ctx) => {

  // فحص الروابط
  if (waitingForLink[ctx.from.id] && ctx.message.text.startsWith("http")) {
    try {
      const response = await axios.head(ctx.message.text);
      await ctx.reply(response.status === 200 ? "✅ الرابط صالح" : "❌ الرابط غير صالح");
    } catch {
      await ctx.reply("❌ فشل فحص الرابط");
    }
    waitingForLink[ctx.from.id] = false;
    return;
  }

  // زخرفة
  if (waitingForDecoration[ctx.from.id]) {
    const name = ctx.message.text;

    const decorated = `
꧁${name}꧂
『${name}』
★彡${name}彡★
꧁༒${name}༒꧂
✿ ${name} ✿
𓆩${name}𓆪
    `;

    await ctx.reply("✨ الزخارف:\n" + decorated);
    waitingForDecoration[ctx.from.id] = false;
    return;
  }

});

/* ================= تشغيل ================= */

bot.launch();
console.log("Bot is running 🚀");

process.once("SIGINT", () => bot.stop("SIGINT"));
process.once("SIGTERM", () => bot.stop("SIGTERM"));

const { Telegraf, Markup } = require("telegraf");
const fs = require("fs");
const axios = require('axios'); // لتفحص الروابط

const bot = new Telegraf(process.env.BOT_TOKEN);

const USERS_FILE = "./users.json";

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

bot.command("restart", async (ctx) => {
  saveUser(ctx.from);
  const userData = getUser(ctx.from.id);

  const profilePhotos = await ctx.telegram.getUserProfilePhotos(ctx.from.id);
  let photo = null;

  if (profilePhotos.total_count > 0) {
    photo = profilePhotos.photos[0][0].file_id;
  }

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
    [Markup.button.callback("🗣 المطور", "dev")],
    [Markup.button.callback("🔗 فحص الروابط", "check_link")],
    [Markup.button.callback("🔄 الاشتراك الإجباري", "mandatory_subscription")]
  ]);

  if (photo) {
    await ctx.replyWithPhoto(photo, { caption, ...buttons });
  } else {
    await ctx.reply(caption, buttons);
  }
});

// فحص الروابط
bot.action("check_link", async (ctx) => {
  ctx.reply("📝 أرسل الرابط الذي تريد فحصه.");
});

bot.on("text", async (ctx) => {
  if (ctx.message.text.startsWith("http")) {
    try {
      const response = await axios.head(ctx.message.text);
      if (response.status === 200) {
        ctx.reply("✅ الرابط صالح.");
      } else {
        ctx.reply("❌ الرابط غير صالح.");
      }
    } catch (error) {
      ctx.reply("❌ حدث خطأ في فحص الرابط.");
    }
  }
});

// فحص الاشتراك الإجباري
bot.action("mandatory_subscription", async (ctx) => {
  const chatId = ctx.chat.id;
  const userId = ctx.from.id;

  const status = await ctx.telegram.getChatMember("@x_1fn", userId);
  if (status.status === 'member' || status.status === 'administrator') {
    ctx.reply("🌟 تم التأكد من اشتراكك في القناة! مرحباً بك في البوت!");
  } else {
    ctx.reply("⚠️ يجب عليك الاشتراك في القناة أولاً: @x_1fn");
  }
});

// التواصل مع المطور
bot.action("dev", (ctx) => {
  ctx.reply("🧑‍💻 تم إرسال طلب التواصل مع المطور.");
  ctx.telegram.sendMessage(7771042305, `📲 مستخدم جديد يريد التواصل: ${ctx.from.first_name}\n🆔 الايدي: ${ctx.from.id}`);
});

// ألعاب
bot.action("games", (ctx) => {
  ctx.reply("🎮 اختر اللعبة:\n1. لعبة التخمين\n2. لعبة الأسئلة العامة\n3. لعبة الأرقام\n4. لعبة القاموس\n5. لعبة الحظ");
});

// فحص الألعاب
bot.action("game_1", (ctx) => {
  ctx.reply("🎮 لعبة التخمين - التخمين بين 1 و 10");
  // يمكنك هنا إضافة اللعبة التفاعلية الخاصة بك
});

bot.action("game_2", (ctx) => {
  ctx.reply("🎮 لعبة الأسئلة العامة - اختر الإجابة الصحيحة");
  // أضف لعبة الأسئلة هنا
});

// لا تنسى إضافة بقية الألعاب المتنوعة بالطريقة نفسها

bot.launch();
console.log("Bot is running 🚀");

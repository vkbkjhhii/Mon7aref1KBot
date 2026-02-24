const { Telegraf, Markup } = require("telegraf");

const bot = new Telegraf(process.env.BOT_TOKEN);

const developerId = 7771042305;
const channelUsername = "@x_1fn";

const pendingSupport = new Map();

// ================== تحقق اشتراك ==================
async function checkSubscription(ctx) {
  try {
    const member = await ctx.telegram.getChatMember(channelUsername, ctx.from.id);
    return ["member", "administrator", "creator"].includes(member.status);
  } catch {
    return false;
  }
}

async function forceSubscribe(ctx) {
  return ctx.reply(
    "🚫 يجب الاشتراك في القناة أولاً لاستخدام البوت",
    Markup.inlineKeyboard([
      [Markup.button.url("📢 اشترك الآن", `https://t.me/x_1fn`)],
      [Markup.button.callback("✅ تحقق من الاشتراك", "check_sub")]
    ])
  );
}

// ================== Start ==================
bot.start(async (ctx) => {
  const subscribed = await checkSubscription(ctx);
  if (!subscribed) return forceSubscribe(ctx);

  ctx.reply(
    "👋 أهلاً بك في البوت الاحترافي\n\nاختر من القائمة:",
    Markup.inlineKeyboard([
      [Markup.button.callback("🔥 إنشاء يوزر مميز", "create_user")],
      [Markup.button.callback("🎮 الألعاب", "games")],
      [Markup.button.callback("📩 تواصل مع المطور", "support")]
    ])
  );
});

bot.action("check_sub", async (ctx) => {
  const subscribed = await checkSubscription(ctx);
  if (subscribed) {
    ctx.editMessageText("✅ تم التحقق بنجاح\nاكتب /start");
  } else {
    ctx.answerCbQuery("❌ لم تشترك بعد", { show_alert: true });
  }
});

// ================== إنشاء يوزر ==================
function generateUsernames(type) {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let results = [];

  for (let i = 0; i < 10; i++) {
    let username = "";
    let length = type === "3" ? 3 : type === "4" ? 4 : 6;
    for (let j = 0; j < length; j++) {
      username += chars[Math.floor(Math.random() * chars.length)];
    }
    results.push("@" + username);
  }
  return results.join("\n");
}

bot.action("create_user", (ctx) => {
  ctx.editMessageText(
    "اختر نوع اليوزر:",
    Markup.inlineKeyboard([
      [Markup.button.callback("ثلاثي", "user_3")],
      [Markup.button.callback("رباعي", "user_4")],
      [Markup.button.callback("عشوائي", "user_random")]
    ])
  );
});

bot.action(/user_(.+)/, (ctx) => {
  const type = ctx.match[1];
  const result = generateUsernames(type === "random" ? "6" : type);
  ctx.reply("🔥 تم توليد 10 يوزرات:\n\n" + result);
});

// ================== الألعاب ==================
bot.action("games", (ctx) => {
  ctx.editMessageText(
    "🎮 اختر لعبة:",
    Markup.inlineKeyboard([
      [Markup.button.callback("❌⭕ لعبة XO", "xo")],
      [Markup.button.callback("🎲 رمي نرد", "dice")],
      [Markup.button.callback("🪙 عملة", "coin")],
      [Markup.button.callback("🔢 رقم عشوائي", "random_number")]
    ])
  );
});

bot.action("dice", (ctx) => ctx.replyWithDice());
bot.action("coin", (ctx) => ctx.reply(Math.random() > 0.5 ? "🪙 وجه" : "🪙 كتابة"));
bot.action("random_number", (ctx) => ctx.reply("🔢 " + Math.floor(Math.random() * 100)));

bot.action("xo", (ctx) => {
  ctx.reply("❌⭕ لعبة XO قادمة في التحديث القادم 🔥");
});

// ================== تواصل مع المطور ==================
bot.action("support", (ctx) => {
  pendingSupport.set(ctx.from.id, true);
  ctx.reply("✍️ اكتب رسالتك الآن وسيتم إرسالها للمطور");
});

bot.on("text", async (ctx) => {
  if (pendingSupport.get(ctx.from.id)) {
    pendingSupport.delete(ctx.from.id);
    await ctx.telegram.sendMessage(
      developerId,
      `📩 رسالة جديدة من:\n\n👤 ${ctx.from.first_name}\n🆔 ${ctx.from.id}\n\n💬 ${ctx.message.text}`
    );
    ctx.reply("✅ تم إرسال رسالتك للمطور");
  }
});

bot.launch();
console.log("Bot Running...");

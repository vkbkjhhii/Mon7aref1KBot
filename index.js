const TelegramBot = require("node-telegram-bot-api");
const axios = require("axios");
const moment = require("moment");

const token = "PUT_BOT_TOKEN";
const OPENAI_KEY = "PUT_OPENAI_KEY";
const ADMIN_ID = 123456789;

const bot = new TelegramBot(token, { polling: true });

let aiSessions = {};
let users = {};
let userState = {};
let banned = new Set();
let lastMessageTime = {};

function mainMenu() {
  return {
    reply_markup: {
      inline_keyboard: [
        [{ text: "🧠 الذكاء الاصطناعي", callback_data: "menu_ai" }],
        [{ text: "🎭 قسم الزخرفة", callback_data: "menu_z" }],
        [{ text: "🔢 قسم التوليد", callback_data: "menu_gen" }],
        [{ text: "👑 قسم اليوزرات", callback_data: "menu_user" }],
        [{ text: "🛡 قسم الحماية", callback_data: "menu_protect" }],
        [{ text: "⚙️ لوحة التحكم", callback_data: "admin" }]
      ]
    }
  };
}

function backBtn() {
  return {
    reply_markup: {
      inline_keyboard: [[{ text: "🔙 رجوع", callback_data: "back" }]]
    }
  };
}

/* ================= START ================= */

bot.onText(/\/start/, async (msg) => {
  const id = msg.from.id;
  if (banned.has(id)) return;

  const name = msg.from.first_name;
  const time = moment().format("YYYY-MM-DD HH:mm:ss");

  users[id] = { join: time };

  try {
    const photos = await bot.getUserProfilePhotos(id);
    if (photos.total_count > 0) {
      const fileId = photos.photos[0][0].file_id;
      await bot.sendPhoto(
        msg.chat.id,
        fileId,
        {
          caption:
`🔥 مرحبًا ${name}
🆔 ID: ${id}
⏰ وقت الدخول: ${time}
🤖 ${bot.me.username}`,
          ...mainMenu()
        }
      );
    } else {
      bot.sendMessage(msg.chat.id,
`🔥 مرحبًا ${name}
🆔 ID: ${id}
⏰ وقت الدخول: ${time}
🤖 ${bot.me.username}`,
        mainMenu()
      );
    }
  } catch {}
});

/* ================= CALLBACK ================= */

bot.on("callback_query", async (q) => {
  const id = q.from.id;
  const msgId = q.message.message_id;
  const chatId = q.message.chat.id;

  if (q.data === "back") {
    return bot.editMessageText("🏠 القائمة الرئيسية", {
      chat_id: chatId,
      message_id: msgId,
      ...mainMenu()
    });
  }

  /* ===== AI ===== */
  if (q.data === "menu_ai") {
    return bot.editMessageText("🧠 قسم الذكاء الاصطناعي", {
      chat_id: chatId,
      message_id: msgId,
      reply_markup: {
        inline_keyboard: [
          [{ text: "💬 تحدث مع AI", callback_data: "ai_start" }],
          [{ text: "🎨 توليد صورة", callback_data: "img" }],
          [{ text: "🖼 تحويل أنمي", callback_data: "anime" }],
          [{ text: "🔙 رجوع", callback_data: "back" }]
        ]
      }
    });
  }

  if (q.data === "ai_start") {
    aiSessions[id] = Date.now();
    bot.editMessageText("✅ بدأ الذكاء الاصطناعي — لديك 10 دقائق", {
      chat_id: chatId,
      message_id: msgId,
      ...backBtn()
    });

    setTimeout(() => {
      delete aiSessions[id];
      bot.sendMessage(chatId, "⏳ انتهت جلسة الذكاء الاصطناعي.");
    }, 600000);
  }

  /* ===== زخرفة ===== */
  if (q.data === "menu_z") {
    return bot.editMessageText("🎭 اختر نوع الزخرفة", {
      chat_id: chatId,
      message_id: msgId,
      reply_markup: {
        inline_keyboard: [
          [{ text: "🇸🇦 عربي", callback_data: "z_ar" }],
          [{ text: "🇬🇧 English", callback_data: "z_en" }],
          [{ text: "🔙 رجوع", callback_data: "back" }]
        ]
      }
    });
  }

  if (q.data === "z_ar" || q.data === "z_en") {
    userState[id] = q.data;
    bot.sendMessage(chatId, "✍️ ارسل الاسم الآن:");
  }

  /* ===== توليد ===== */
  if (q.data === "menu_gen") {
    return bot.editMessageText("🔢 قسم التوليد", {
      chat_id: chatId,
      message_id: msgId,
      reply_markup: {
        inline_keyboard: [
          [{ text: "🔐 توليد باسورد", callback_data: "pass" }],
          [{ text: "📧 توليد ايميل", callback_data: "email" }],
          [{ text: "🌐 أرقام فيك", callback_data: "fake" }],
          [{ text: "🔙 رجوع", callback_data: "back" }]
        ]
      }
    });
  }

  if (q.data === "fake") {
    const num = "+1" + Math.floor(Math.random() * 9000000000);
    bot.editMessageText(`🌐 رقم فيك:\n${num}`, {
      chat_id: chatId,
      message_id: msgId,
      reply_markup: {
        inline_keyboard: [
          [{ text: "🔄 رقم جديد", callback_data: "fake" }],
          [{ text: "🔙 رجوع", callback_data: "back" }]
        ]
      }
    });
  }

  /* ===== يوزرات ===== */
  if (q.data === "menu_user") {
    let list = "";
    for (let i = 0; i < 15; i++) {
      list += `@Elite_${Math.random().toString(36).substring(2,6)}\n`;
    }
    bot.editMessageText("👑 يوزرات مميزة:\n\n" + list, {
      chat_id: chatId,
      message_id: msgId,
      ...backBtn()
    });
  }

  /* ===== حماية ===== */
  if (q.data === "menu_protect") {
    bot.editMessageText("🛡 نظام حماية مفعل", {
      chat_id: chatId,
      message_id: msgId,
      ...backBtn()
    });
  }

  /* ===== ادمن ===== */
  if (q.data === "admin") {
    if (id != ADMIN_ID)
      return bot.answerCallbackQuery(q.id, { text: "❌ ليس لديك صلاحية", show_alert: true });

    bot.editMessageText("⚙️ لوحة التحكم", {
      chat_id: chatId,
      message_id: msgId,
      reply_markup: {
        inline_keyboard: [
          [{ text: "📢 إذاعة", callback_data: "broadcast" }],
          [{ text: "📈 عدد المستخدمين", callback_data: "count" }],
          [{ text: "🔙 رجوع", callback_data: "back" }]
        ]
      }
    });
  }

  if (q.data === "count") {
    bot.answerCallbackQuery(q.id, {
      text: `👥 عدد المستخدمين: ${Object.keys(users).length}`,
      show_alert: true
    });
  }
});

/* ================= الرسائل ================= */

bot.on("message", async (msg) => {
  const id = msg.from.id;
  if (banned.has(id)) return;

  // Anti Flood
  if (lastMessageTime[id] && Date.now() - lastMessageTime[id] < 1000)
    return;
  lastMessageTime[id] = Date.now();

  // زخرفة
  if (userState[id]) {
    const name = msg.text;
    let result = "";
    for (let i = 0; i < 10; i++) {
      result += `✨ ${name}_${Math.random().toString(36).substring(2,4)}\n`;
    }
    bot.sendMessage(msg.chat.id, "🎭 الزخرفة:\n\n" + result);
    delete userState[id];
  }

  // AI
  if (aiSessions[id]) {
    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-4o-mini",
          messages: [{ role: "user", content: msg.text }]
        },
        {
          headers: { Authorization: `Bearer ${OPENAI_KEY}` }
        }
      );

      bot.sendMessage(msg.chat.id, response.data.choices[0].message.content);
    } catch {
      bot.sendMessage(msg.chat.id, "⚠️ خطأ في الذكاء الاصطناعي");
    }
  }
});

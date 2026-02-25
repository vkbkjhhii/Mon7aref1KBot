const { Telegraf, Markup } = require("telegraf");
const axios = require("axios");
const moment = require("moment");
const fs = require("fs-extra");

const bot = new Telegraf(process.env.TOKEN);
const CHANNEL = process.env.CHANNEL;
const DEV_ID = Number(process.env.DEV_ID);
const DEV_USER = process.env.DEV_USER;
const OPENAI_KEY = process.env.OPENAI_KEY || "";

let usedUsers = new Set();
let fakeCache = {};
let styleWait = {};
let aiWait = {};
let xoGames = {};

// ===== اشتراك إجباري =====
async function checkSub(ctx){
  try{
    const m = await ctx.telegram.getChatMember(CHANNEL, ctx.from.id);
    return ["creator","administrator","member"].includes(m.status);
  }catch{ return false; }
}

async function forceSub(ctx){
  const ok = await checkSub(ctx);
  if(ok) return true;
  await ctx.reply("⚠️ لازم تشترك في القناة أولاً",
    Markup.inlineKeyboard([
      [Markup.button.url("اشترك الآن", `https://t.me/${CHANNEL.replace("@","")}`)],
      [Markup.button.callback("تحقق", "checksub")]
    ])
  );
  return false;
}

bot.action("checksub", async (ctx)=>{
  const ok = await checkSub(ctx);
  if(ok){ ctx.answerCbQuery("تم التحقق ✅"); ctx.deleteMessage(); }
  else ctx.answerCbQuery("لسه مش مشترك ❌");
});

// ===== START =====
bot.start(async (ctx)=>{
  if(!(await forceSub(ctx))) return;

  const photos = await ctx.telegram.getUserProfilePhotos(ctx.from.id);
  const photo = photos.total_count ? photos.photos[0][0].file_id : null;
  const time = moment().format("YYYY-MM-DD HH:mm:ss");

  const caption =
`𓂀 𝐀𝐋𝐌𝐍𝐇𝐑𝐅 𓂀

👤 Name :
${ctx.from.first_name}

🔗 Username :
@${ctx.from.username || "None"}

🆔 ID :
${ctx.from.id}

⏰ Time :
${time}

━━━━━━━━━━━━━━

أهلاً بك 👑
أنت الآن مستخدم في البوت الخاص بنا`;

  const keyboard = Markup.inlineKeyboard([
    [
      Markup.button.callback("📱 أرقام فيك","fake"),
      Markup.button.callback("👑 User مميز","user")
    ],
    [
      Markup.button.callback("✨ زخرفة","style"),
      Markup.button.callback("🎮 XO","xo")
    ],
    [
      Markup.button.callback("🤖 ذكاء اصطناعي","ai"),
      Markup.button.callback("👨‍💻 المطور","dev")
    ]
  ]);

  if(photo) ctx.replyWithPhoto(photo,{caption,...keyboard});
  else ctx.reply(caption,keyboard);
});

// ===== أرقام فيك =====
const countries = ["Egypt","Yemen","UAE","Saudi","Qatar","Kuwait","Oman","Bahrain",
"USA","UK","Germany","France","Italy","Spain","Turkey","India","China","Japan","Brazil","Canada"];

function genNum(){
  return "+20"+Math.floor(100000000+Math.random()*900000000);
}

bot.action("fake",(ctx)=>{
  const btn = countries.map(c=>[Markup.button.callback(c,"c_"+c)]);
  ctx.editMessageText("🌍 اختر الدولة",Markup.inlineKeyboard(btn));
});

bot.action(/c_(.+)/,(ctx)=>{
  const num = genNum();
  fakeCache[ctx.from.id]=num;
  ctx.editMessageText(
`📱 الرقم :

${num}`,
  Markup.inlineKeyboard([
    [Markup.button.callback("🔄 تغيير الرقم","chg")],
    [Markup.button.callback("📩 طلب كود","code")]
  ]));
});

bot.action("chg",(ctx)=>{
  const num = genNum();
  fakeCache[ctx.from.id]=num;
  ctx.editMessageText(
`📱 الرقم :

${num}`,
  Markup.inlineKeyboard([
    [Markup.button.callback("🔄 تغيير الرقم","chg")],
    [Markup.button.callback("📩 طلب كود","code")]
  ]));
});

bot.action("code",(ctx)=>{
  const code = Math.floor(100000+Math.random()*900000);
  ctx.answerCbQuery();
  ctx.reply(`🔐 كودك العشوائي:\n\n${code}`);
});

// ===== User مميز =====
function randomUser(len){
  const chars="abcdefghijklmnopqrstuvwxyz";
  let u="";
  while(u.length<len){
    const c=chars[Math.floor(Math.random()*chars.length)];
    u+=c;
  }
  if(usedUsers.has(u)) return randomUser(len);
  usedUsers.add(u);
  return u;
}

bot.action("user",(ctx)=>{
  ctx.editMessageText("اختر النوع",
  Markup.inlineKeyboard([
    [Markup.button.callback("ثلاثي","u3")],
    [Markup.button.callback("رباعي","u4")]
  ]));
});

bot.action(/u(3|4)/,(ctx)=>{
  const len=Number(ctx.match[1]);
  let list="";
  for(let i=0;i<10;i++) list+=`@${randomUser(len)}\n`;
  ctx.editMessageText("👑 أفضل 10 يوزرات:\n\n"+list);
});

// ===== زخرفة =====
bot.action("style",(ctx)=>{
  ctx.editMessageText("اختر اللغة",
  Markup.inlineKeyboard([
    [Markup.button.callback("عربي","ar")],
    [Markup.button.callback("English","en")]
  ]));
});

bot.action(/ar|en/,(ctx)=>{
  styleWait[ctx.from.id]=ctx.callbackQuery.data;
  ctx.reply("أرسل الاسم الآن ✍️");
});

bot.on("text",(ctx)=>{
  if(styleWait[ctx.from.id]){
    const name=ctx.message.text;
    delete styleWait[ctx.from.id];
    const list=
`★彡${name}彡★

꧁${name}꧂

𓆩${name}𓆪

『${name}』

✿${name}✿

๖${name}๖

༺${name}༻

۝${name}۝

♛${name}♛

♔${name}♔`;
    return ctx.reply("✨ زخارف احترافية:\n\n"+list);
  }

  if(aiWait[ctx.from.id] && OPENAI_KEY){
    axios.post("https://api.openai.com/v1/chat/completions",{
      model:"gpt-3.5-turbo",
      messages:[{role:"user",content:ctx.message.text}]
    },{
      headers:{Authorization:`Bearer ${OPENAI_KEY}`}
    }).then(r=>{
      ctx.reply(r.data.choices[0].message.content);
    }).catch(()=>ctx.reply("حصل خطأ في AI"));
    return;
  }
});

// ===== AI =====
bot.action("ai",(ctx)=>{
  if(!OPENAI_KEY) return ctx.answerCbQuery("لم يتم ضبط API ❌",true);
  aiWait[ctx.from.id]=true;
  ctx.reply("اكتب سؤالك الآن 🤖");
});

// ===== XO =====
bot.action("xo",(ctx)=>{
  xoGames[ctx.from.id]=Array(9).fill("-");
  drawXO(ctx);
});

function drawXO(ctx){
  const b=xoGames[ctx.from.id];
  const btn=[];
  for(let i=0;i<9;i+=3){
    btn.push([
      Markup.button.callback(b[i],"x"+i),
      Markup.button.callback(b[i+1],"x"+(i+1)),
      Markup.button.callback(b[i+2],"x"+(i+2))
    ]);
  }
  ctx.editMessageText("🎮 XO",Markup.inlineKeyboard(btn));
}

bot.action(/x(\d)/,(ctx)=>{
  const i=Number(ctx.match[1]);
  if(xoGames[ctx.from.id][i]==="-"){
    xoGames[ctx.from.id][i]="X";
    const empty=xoGames[ctx.from.id].map((v,i)=>v==="-"?i:null).filter(v=>v!==null);
    if(empty.length){
      const r=empty[Math.floor(Math.random()*empty.length)];
      xoGames[ctx.from.id][r]="O";
    }
  }
  drawXO(ctx);
});

// ===== المطور =====
bot.action("dev",(ctx)=>{
  ctx.editMessageText(
`👑 أقوى مطور مصري

خبرة عالية في برمجة البوتات

ID : ${DEV_ID}`,
  Markup.inlineKeyboard([
    [Markup.button.url("تواصل مع المطور",`https://t.me/${DEV_USER}`)]
  ]));
});

bot.launch();
console.log("Bot Started");

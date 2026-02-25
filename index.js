const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply(
    "اختر من الزرار 👇",
    Markup.keyboard([
      ["📺 قنوات التليفزيون"]
    ]).resize()
  );
});

bot.hears("📺 قنوات التليفزيون", (ctx) => {
  ctx.reply(`
🔗 https://5b622f07944df.streamlock.net/aghapy.tv/aghapy.smil/playlist.m3u8

🔹 Al Ghad TV (1080p)
🔗 https://eazyvwqssi.erbvr.com/alghadtv/alghadtv.m3u8

🔹 Al Masriyah [Geo-Blocked]
🔗 https://viamotionhsi.netplus.ch/live/eds/almasriyah/browser-HLS8/almasriyah.m3u8

🔹 ATVSat (1080p) [Not 24/7]
🔗 https://stream.atvsat.com/atvsatlive/smil:atvsatlive.smil/playlist.m3u8

🔹 CBC (576p)
🔗 https://flu.systemnet.tv/CBC/index.m3u8

🔹 CBC Drama (576p)
🔗 https://flu.systemnet.tv/CBCDrama/index.m3u8

🔹 CBC Sofra (576p)
🔗 https://flu.systemnet.tv/CBCSofra/index.m3u8

🔹 Coptic TV (720p) [Not 24/7]
🔗 https://5aafcc5de91f1.streamlock.net/ctvchannel.tv/ctv.smil/playlist.m3u8

🔹 El Radio 9090 FM (480p)
🔗 https://9090video.mobtada.com/hls/stream.m3u8

🔹 Elbeshara GTV (1080p) [Not 24/7]
🔗 http://media3.smc-host.com:1935/elbesharagtv.com/gtv.smil/playlist.m3u8

🔹 Huda TV (720p) [Not 24/7]
🔗 https://cdn.bestream.io:19360/elfaro1/elfaro1.m3u8

🔹 Koogi TV (1080p)
🔗 https://5d658d7e9f562.streamlock.net/koogi.tv/koogi.smil/playlist.m3u8

🔹 MBC 1 Egypt (1080p)
🔗 https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-1-na/eec141533c90dd34722c503a296dd0d8/index.m3u8

🔹 MBC Masr (1080p)
🔗 https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-masr/956eac069c78a35d47245db6cdbb1575/index.m3u8

🔹 MBC Masr 2 (1080p)
🔗 https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-masr-2/754931856515075b0aabf0e583495c68/index.m3u8

🔹 MBC Masr Drama (1080p)
🔗 https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-masr-drama/567b703c19ede6598222de81b0e4508b/index.m3u8

🔹 Mekameleen TV (1080p)
🔗 https://mn-nl.mncdn.com/mekameleen/smil:mekameleentv.smil/playlist.m3u8

🔹 Mix Hollywood (1080p)
🔗 https://ml-pull-hwc.myco.io/MixTV/hls/index.m3u8

🔹 NogoumFMTV (672p) [Not 24/7]
🔗 https://nogoumtv.nrpstream.com/hls/stream.m3u8

🔹 PNC Drama
🔗 https://d35j504z0x2vu2.cloudfront.net/v1/master/0bc8e8376bd8417a1b6761138aa41c26c7309312/pnc-drama/master.m3u8?ads.vf=xdliEBYtdWS

🔹 Watan TV (1080p)
🔗 https://rp.tactivemedia.com/watantv_source/live/playlist.m3u8
`);
});

bot.launch();

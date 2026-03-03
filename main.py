import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# ---------------- تحميل هكر موحد ----------------

async def hacker_loading(message, title="Processing"):
    for i in range(1, 101):
        bar_length = 20
        filled = int(bar_length * i / 100)
        empty = bar_length - filled
        bar = "█" * filled + "░" * empty
        await asyncio.sleep(0.02)
        await message.edit_text(
            f"💀 <b>{title}</b>\n"
            f"[{bar}] {i}%"
        )

# ---------------- توليد بيانات تجريبية ----------------

banks = ["Secure Demo Bank", "Virtual Trust Bank", "Neo Digital Bank"]
types_cards = ["VISA - TEST MODE", "VISA - DEMO", "VISA - SANDBOX"]
countries = [("USA 🇺🇸", "$"), ("UK 🇬🇧", "£"), ("Germany 🇩🇪", "€")]

def generate_fake_data():
    card_id = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) + "-" + \
              ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) + "-" + \
              ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))

    expiry = f"{random.randint(1,12):02d}/20XX"
    value = random.randint(10, 100)

    country, currency = random.choice(countries)

    return f"""
𝗣𝗮𝘀𝘀𝗲𝗱 ✅

[-] Card ID : {card_id}
[-] Expiry : {expiry}
[-] CVV : ***
[-] Bank : {random.choice(banks)}
[-] Card Type : {random.choice(types_cards)}
[-] Country : {country}
[-] Value : {currency}{value}

============================
[-] by : DEMO BOT
"""

# ---------------- القائمة الرئيسية ----------------

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📱 Fake Number", callback_data="fake"),
        InlineKeyboardButton("👑 VIP", callback_data="vip"),
        InlineKeyboardButton("🔗 Check Link", callback_data="check"),
        InlineKeyboardButton("🎮 XO Game", callback_data="xo"),
        InlineKeyboardButton("💳 Secure Generator", callback_data="secure_gen"),
        InlineKeyboardButton("📩 Contact Dev", url="https://t.me/yourusername")
    )
    return kb

# ---------------- أوامر ----------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("🔥 Welcome To The Bot 🔥", reply_markup=main_menu())

# ---------------- زر Secure Generator ----------------

@dp.callback_query_handler(lambda c: c.data == "secure_gen")
async def secure_generator(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("💀 Generating Secure Data... 0%")
    await hacker_loading(msg, "Generating Secure Data")
    await msg.edit_text("<b>ACCESS GRANTED ☠️</b>")
    await asyncio.sleep(1)
    await msg.edit_text(generate_fake_data(), reply_markup=main_menu())

# ---------------- أزرار تجريبية لباقي القوائم ----------------

@dp.callback_query_handler(lambda c: c.data == "fake")
async def fake_number(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("💀 Opening Server... 0%")
    await hacker_loading(msg, "Opening Virtual Server")
    await msg.edit_text("📱 +20 10" + str(random.randint(10000000,99999999)),
                        reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "vip")
async def vip_menu(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("💀 Accessing VIP... 0%")
    await hacker_loading(msg, "VIP Access")
    await msg.edit_text("👑 VIP ACCESS GRANTED", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "check")
async def check_link(callback: types.CallbackQuery):
    msg = await callback.message.edit_text("💀 Scanning Link... 0%")
    await hacker_loading(msg, "Scanning Link")
    await msg.edit_text("🔗 Link Is Safe ✅", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "xo")
async def xo_game(callback: types.CallbackQuery):
    await callback.message.edit_text("🎮 XO Game Coming Soon 🔥",
                                     reply_markup=main_menu())

# ---------------- تشغيل ----------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

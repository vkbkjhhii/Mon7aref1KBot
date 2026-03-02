# ----------- توليد الرقم مع شريط تحميل متحرك -----------
@dp.callback_query_handler(lambda c: c.data.startswith("country_"))
async def send_number(callback_query: types.CallbackQuery):
    country_key = callback_query.data.split("_")[1]
    country_name, country_code = countries[country_key]

    # رسالة البداية للتحميل
    msg = await callback_query.message.edit_text("🔹 جاري انشاء الرقم...")

    # شريط تحميل متحرك
    progress = ["🔹▫▫▫▫▫", "🔹🔹▫▫▫▫", "🔹🔹🔹▫▫▫", "🔹🔹🔹🔹▫▫", "🔹🔹🔹🔹🔹▫", "🔹🔹🔹🔹🔹🔹"]
    for p in progress:
        await asyncio.sleep(1)
        await msg.edit_text(f"⏳ إنشاء الرقم:\n{p}")

    # بعد انتهاء التحميل
    number = generate_number(country_code)
    now = datetime.datetime.now()

    text = f"""
➖ تم انشاء الرقم 🛎•
➖ رقم الهاتف ☎️ : <code>{number}</code>
➖ الدوله : {country_name}
➖ رمز الدوله 🌏 : {country_code}
➖ المنصه 🔮 : لجميع الموقع والبرامج
➖ تاريج الانشاء 📅 : {now.strftime('%Y-%m-%d')}
➖ وقت الانشاء ⏰ : {now.strftime('%I:%M %p')}
➖ اضغط ع الرقم لنسخه.
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 تغير الرقم", callback_data=f"country_{country_key}")
    )
    keyboard.add(
        InlineKeyboardButton("💬 طلب الكود", callback_data="get_code")
    )

    await msg.edit_text(text, reply_markup=keyboard)

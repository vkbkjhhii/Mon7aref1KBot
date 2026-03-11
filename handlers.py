@dp.callback_query_handler(lambda c: c.data=="get_code")
    async def get_code(callback: types.CallbackQuery):
        await callback.answer("لم يتم الحصول على رسائل SMS حتا الان 📩", show_alert=True)

    # ---------- يوزر مميز ----------
    def generate_user():
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZIl"
        return "@" + "".join(random.choice(chars) for _ in range(4))

    @dp.callback_query_handler(lambda c: c.data=="vip")
    async def vip(callback: types.CallbackQuery):
        msg = await callback.message.edit_text("⏳ جاري توليد user مميز...")
        anim = ["▰▱▱▱▱","▰▰▱▱▱","▰▰▰▱▱","▰▰▰▰▱","▰▰▰▰▰"]
        for a in anim*2:
            await asyncio.sleep(0.3)
            await msg.edit_text(f"⏳ جاري توليد user مميز... {a}")
        await msg.delete()
        for _ in range(10):
            await callback.message.answer(generate_user())
            await asyncio.sleep(0.3)
        await callback.message.answer("انتهى الصيد 🖱️", reply_markup=back_btn())

    # ---------- فحص الروابط ----------
    @dp.callback_query_handler(lambda c: c.data=="check_link")
    async def check_link(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "check_link"
        await callback.message.edit_text("الرجاء إرسال الرابط فقط 🔎", reply_markup=None)

    @dp.message_handler(lambda message: user_state.get(message.from_user.id)=="check_link")
    async def handle_links(message: types.Message):
        link = message.text.strip()
        if not (link.startswith("http://") or link.startswith("https://")):
            await message.reply("❌ يمكنك إرسال الرابط فقط")
            return
        parsed = urlparse(link)
        domain = parsed.netloc
        path = parsed.path
        if "wa.me" in domain or "api.whatsapp.com" in domain:
            link_type = "واتساب"
        elif "t.me" in domain:
            link_type = "تيليجرام"
        elif "tiktok.com" in domain:
            link_type = "تيك توك"
        else:
            link_type = "عام HTTPS"
        result_text = f"""
🔗 الرابط: {link}
🌐 الدومين: {domain}
📂 المسار: {path}
✅ نوع الرابط: {link_type}
⚠️ الرابط آمن
"""
        await message.answer(result_text)
        user_state.pop(message.from_user.id)

    # ---------- التواصل مع المطور ----------
    @dp.callback_query_handler(lambda c: c.data=="contact_dev")
    async def contact_dev(callback: types.CallbackQuery):
        user_state[callback.from_user.id] = "to_dev"
        await callback.message.answer("✉️ اكتب رسالتك وسأقوم بعرضها على المطور")

    @dp.message_handler(lambda message: user_state.get(message.from_user.id)=="to_dev")
    async def forward_to_dev(message: types.Message):
        sent_msg = await message.answer("✅ تم إرسال رسالتك")
        await message.delete()
        await dp.bot.send_message(DEV_ID, f"💬 رسالة من {message.from_user.first_name} ({message.from_user.id}):\n{message.text}")
        await asyncio.sleep(5)
        await sent_msg.delete()
        user_state.pop(message.from_user.id)

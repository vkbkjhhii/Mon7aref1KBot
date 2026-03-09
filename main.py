# ---------------- وضع الصيانة ----------------

maintenance_users = set()

@dp.message_handler(lambda message: message.text and message.text.lower() == "restart")
async def restart_mode(message: types.Message):

    maintenance_users.add(message.from_user.id)

    user = message.from_user
    name = user.first_name

    photos = await bot.get_user_profile_photos(user.id)

    text = f"""
عزيزي المستخدم {name} 👋

⚙️ البوت حالياً تحت الصيانة.

سيتم اصلاح البوت قريباً
وسيتم اشعارك عند عودة الخدمة.

شكراً لصبرك ❤️
"""

    if photos.total_count > 0:
        photo_id = photos.photos[0][-1].file_id
        await message.answer_photo(photo_id, caption=text)
    else:
        await message.answer(text)


@dp.message_handler(lambda message: message.from_user.id in maintenance_users)
async def maintenance_filter(message: types.Message):

    try:
        await message.delete()
    except:
        pass

    name = message.from_user.first_name

    text = f"""
عزيزي المستخدم {name}

⚙️ البوت تحت الصيانة حالياً.

يرجى المحاولة لاحقاً.
"""

    await message.answer(text)

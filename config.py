import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN مش موجود ❌")

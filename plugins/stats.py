from pyrogram import Client, filters
from data import users_data

# Apna Telegram User ID yahan daalo
OWNER_ID = 8229785450


@Client.on_message(filters.private & filters.command("stats"))
async def stats_cmd(_, message):
    if message.from_user.id != OWNER_ID:
        return

    active_sessions = len(users_data)

    await message.reply_text(
        "📊 Bot Statistics\n\n"
        f"⚡ Active Sessions: {active_sessions}\n"
        f"💾 Session Records: {active_sessions}"
    )

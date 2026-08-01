from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup

from data import Data


@Client.on_message(filters.private & filters.command("start"))
async def start_command(_, message):
    await message.reply_text(
        "Welcome to String Session Generator Bot.\n\n"
        "Click the button below to continue.",
        reply_markup=InlineKeyboardMarkup(Data.start_buttons)
    )

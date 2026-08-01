from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup
)

from data import Data


@Client.on_callback_query()
async def callbacks(_, query: CallbackQuery):

    data = query.data

    if data == "home":
        await query.message.edit_text(
            "Welcome to String Session Generator Bot.\n\n"
            "Click the button below to continue.",
            reply_markup=InlineKeyboardMarkup(Data.start_buttons)
        )

    elif data == "generate":
        await query.message.edit_text(
            "Select a library.",
            reply_markup=InlineKeyboardMarkup(
                Data.generate_buttons
            )
        )

    elif data == "pyrogram":
        await query.message.edit_text(
            "Select Pyrogram version.",
            reply_markup=InlineKeyboardMarkup(
                Data.pyrogram_buttons
            )
        )

    elif data == "telethon":
        await query.message.edit_text(
            "Select Telethon version.",
            reply_markup=InlineKeyboardMarkup(
                Data.telethon_buttons
            )
        )

    await query.answer()

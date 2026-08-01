from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from data import Data


@Client.on_callback_query()
async def callbacks(_, query: CallbackQuery):
    data = query.data

    try:
        if data == "home":
            await query.message.edit_text(
                Data.START_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    Data.START_BUTTONS
                )
            )

        elif data == "generate":
            await query.message.edit_text(
                Data.GENERATE_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    Data.GENERATE_BUTTONS
                )
            )

        elif data == "pyrogram":
            await query.message.edit_text(
                Data.PYROGRAM_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    Data.PYROGRAM_BUTTONS
                )
            )

        elif data == "telethon":
            await query.message.edit_text(
                Data.TELETHON_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    Data.TELETHON_BUTTONS
                )
            )

        elif data == "pyrogram_v2":
            await query.message.edit_text(
                "Pyrogram V2 selected.\n\n"
                "Send your API_ID."
            )

        elif data == "pyrogram_v3":
            await query.message.edit_text(
                "Pyrogram V3 selected.\n\n"
                "Send your API_ID."
            )

        elif data == "telethon_v2":
            await query.message.edit_text(
                "Telethon V2 selected.\n\n"
                "Send your API_ID."
            )

        elif data == "telethon_v3":
            await query.message.edit_text(
                "Telethon V3 selected.\n\n"
                "Send your API_ID."
            )

        await query.answer()

    except Exception as e:
        await query.answer(
            str(e),
            show_alert=True
        )

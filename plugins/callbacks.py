from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from data import users_data, save_users_data, Data
from plugins.states import STATE_INPUT_1

@Client.on_callback_query(filters.regex("pyrogram_v2"))
async def pyrogram_v2_chosen(_, query: CallbackQuery):
    user_id = query.from_user.id
    users_data[user_id] = {"step": STATE_INPUT_1}
    save_users_data()
    await query.message.edit_text(
        f"{Data.PYROGRAM_TEXT} v2\n\nSend your first parameter (e.g., API_ID):"
    )
    await query.answer()

@Client.on_callback_query(filters.regex("pyrogram_v3"))
async def pyrogram_v3_chosen(_, query: CallbackQuery):
    user_id = query.from_user.id
    users_data[user_id] = {"step": STATE_INPUT_1}
    save_users_data()
    await query.message.edit_text(
        f"{Data.PYROGRAM_TEXT} v3\n\nSend your first parameter (e.g., API_ID):"
    )
    await query.answer()

@Client.on_callback_query(filters.regex("telethon_v2"))
async def telethon_v2_chosen(_, query: CallbackQuery):
    user_id = query.from_user.id
    users_data[user_id] = {"step": STATE_INPUT_1}
    save_users_data()
    await query.message.edit_text(
        f"{Data.TELETHON_TEXT} v2\n\nSend your first parameter (e.g., API_ID):"
    )
    await query.answer()

@Client.on_callback_query(filters.regex("telethon_v3"))
async def telethon_v3_chosen(_, query: CallbackQuery):
    user_id = query.from_user.id
    users_data[user_id] = {"step": STATE_INPUT_1}
    save_users_data()
    await query.message.edit_text(
        f"{Data.TELETHON_TEXT} v3\n\nSend your first parameter (e.g., API_ID):"
    )
    await query.answer()

# (other callbacks for home, generate, etc. can be added similarly)

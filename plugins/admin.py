"""
plugins/admin.py – Admin commands (owner only).

/broadcast <text>  – Send a message to all users who ever started the bot.
/stats             – Show total users, active sessions, etc.
"""

import json
import os
import logging
from pathlib import Path
from typing import Set

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from data import users_data   # for active state count

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
#  Broadcast user list persistence (atomic JSON)
# ---------------------------------------------------------------------------
BROADCAST_FILE = Path("broadcast_users.json")
BROADCAST_TEMP = Path("broadcast_users.json.tmp")

broadcast_users: Set[int] = set()


def load_broadcast_users():
    """Load the set of user IDs from disk."""
    global broadcast_users
    if BROADCAST_FILE.exists():
        try:
            with open(BROADCAST_FILE, encoding="utf-8") as f:
                raw = json.load(f)
            broadcast_users = {int(uid) for uid in raw}
        except Exception:
            logger.exception("Corrupted broadcast_users.json, starting fresh.")
            broadcast_users = set()
    else:
        broadcast_users = set()


def save_broadcast_users():
    """Atomically write the broadcast user set to disk."""
    with open(BROADCAST_TEMP, "w", encoding="utf-8") as f:
        json.dump(list(broadcast_users), f)
    os.replace(BROADCAST_TEMP, BROADCAST_FILE)


def add_broadcast_user(user_id: int):
    """Add a user to the broadcast list. Call this from start.py."""
    if user_id not in broadcast_users:
        broadcast_users.add(user_id)
        save_broadcast_users()


# Load existing list on import
load_broadcast_users()


# ---------------------------------------------------------------------------
#  Owner‑only filter (reusable)
# ---------------------------------------------------------------------------
def owner_only(_, __, message: Message) -> bool:
    return message.from_user.id == OWNER_ID


owner_filter = filters.create(owner_only)


# ---------------------------------------------------------------------------
#  /broadcast – Send a message to all tracked users
# ---------------------------------------------------------------------------
@Client.on_message(filters.command("broadcast") & filters.private & owner_filter)
async def broadcast(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/broadcast <text>`")
        return

    text = message.text.split(None, 1)[1]
    total = len(broadcast_users)
    if total == 0:
        await message.reply_text("No users in broadcast list yet.")
        return

    await message.reply_text(f"Broadcasting to {total} users...")

    success = 0
    fail = 0
    for uid in broadcast_users:
        try:
            await client.send_message(uid, text)
            success += 1
        except Exception as e:
            logger.warning("Failed to send to %d: %s", uid, e)
            fail += 1

    await message.reply_text(
        f"✅ Broadcast finished.\n"
        f"• Sent: {success}\n"
        f"• Failed: {fail}"
    )


# ---------------------------------------------------------------------------
#  /stats – Show bot statistics
# ---------------------------------------------------------------------------
@Client.on_message(filters.command("stats") & filters.private & owner_filter)
async def stats(_, message: Message):
    active_sessions = len(users_data)
    total_users = len(broadcast_users)
    await message.reply_text(
        f"📊 **Bot Statistics**\n\n"
        f"• Total users (ever): {total_users}\n"
        f"• Active sessions: {active_sessions}"
    )

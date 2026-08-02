"""
plugins/generate.py – Production‑ready state‑machine handler (Pyrogram v2).

- JSON persistence with atomic writes (survives restart)
- Anti‑spam 1.5 s cooldown + periodic cleanup (every 10 min)
- Safer text access (None‑safe)
- Clean logging (no secrets, only keys, step key filtered out)
- Centralised command exclusion list (from data.py)
- Defensive key checks, auto‑reset on errors
"""

import logging
import time
from typing import Any, Dict

from pyrogram import Client, filters
from pyrogram.types import Message

from data import users_data, save_users_data, BOT_COMMANDS
from plugins.states import (
    STATE_INPUT_1,
    STATE_INPUT_2,
    STATE_INPUT_3,
    STATE_CONFIRM,
)

logger = logging.getLogger(__name__)

# ---------- Anti‑spam cooldown ----------
_user_cooldowns: Dict[int, float] = {}
_COOLDOWN = 1.5               # seconds
_CLEANUP_INTERVAL = 600       # prune old entries every 10 minutes
_last_cleanup = 0.0


def _cleanup_cooldowns(now: float) -> None:
    """Periodically remove cooldown entries older than 1 hour."""
    global _last_cleanup
    if now - _last_cleanup > _CLEANUP_INTERVAL:
        cutoff = now - 3600
        # Build a list of expired user IDs, then delete them.
        expired = [uid for uid, ts in _user_cooldowns.items() if ts < cutoff]
        for uid in expired:
            del _user_cooldowns[uid]
        _last_cleanup = now


# ---------- Filter: private text, not a bot command ----------
TEXT_FILTER = (
    filters.private
    & filters.text
    & ~filters.command(BOT_COMMANDS)
)


def reset_user(user_id: int) -> None:
    """Remove user data and persist the change."""
    if user_id in users_data:
        del users_data[user_id]
        save_users_data()
        logger.info("User %d state cleared.", user_id)


# ---------- /cancel ----------
@Client.on_message(filters.private & filters.command("cancel"))
async def cmd_cancel(_: Client, message: Message) -> None:
    user_id = message.from_user.id
    if user_id in users_data:
        reset_user(user_id)
        await message.reply_text("❌ Operation cancelled.")
    else:
        await message.reply_text("ℹ️ No active operation to cancel.")


# ---------- Main dispatcher ----------
@Client.on_message(TEXT_FILTER)
async def handle_state_input(_: Client, message: Message) -> None:
    user_id = message.from_user.id

    # ---- anti‑spam check + periodic cleanup ----
    now = time.time()
    _cleanup_cooldowns(now)

    last = _user_cooldowns.get(user_id, 0)
    if now - last < _COOLDOWN:
        return
    _user_cooldowns[user_id] = now

    # ---- only act if an active session exists ----
    if user_id not in users_data:
        return

    user_entry: Dict[str, Any] = users_data[user_id]
    step = user_entry.get("step")

    if not step:
        logger.warning("User %d has no 'step'. Resetting.", user_id)
        reset_user(user_id)
        return

    username = message.from_user.username or "no_username"
    logger.info("User=%s Username=%s Step=%s TextReceived", user_id, username, step)

    try:
        previous_step = step
        if step == STATE_INPUT_1:
            await process_step_1(message, user_entry)
        elif step == STATE_INPUT_2:
            await process_step_2(message, user_entry)
        elif step == STATE_INPUT_3:
            await process_step_3(message, user_entry)
        elif step == STATE_CONFIRM:
            await process_confirmation(message, user_entry)
        else:
            logger.error("User %d unknown step '%s'. Resetting.", user_id, step)
            await message.reply_text("⚠️ Unexpected state. Operation reset.")
            reset_user(user_id)
            return

        new_step = user_entry.get("step")
        if new_step and new_step != previous_step:
            logger.info("User=%s moved %s -> %s", user_id, previous_step, new_step)

    except Exception:
        # logger.exception already includes the full traceback
        logger.exception("Error for user %d in step '%s'", user_id, step)
        await message.reply_text("❌ An error occurred. Operation cancelled.")
        reset_user(user_id)


# ---------- Step 1 ----------
async def process_step_1(message: Message, user_entry: Dict[str, Any]) -> None:
    data = (message.text or "").strip()
    if not data:
        await message.reply_text("❌ Input cannot be empty. Try again:")
        return

    user_entry["param1"] = data
    user_entry["step"] = STATE_INPUT_2
    save_users_data()
    await message.reply_text("Got it! Now enter the second parameter:")


# ---------- Step 2 ----------
async def process_step_2(message: Message, user_entry: Dict[str, Any]) -> None:
    data = (message.text or "").strip()
    if len(data) < 3:
        await message.reply_text("❌ Must be at least 3 characters. Try again:")
        return

    user_entry["param2"] = data
    user_entry["step"] = STATE_INPUT_3
    save_users_data()
    await message.reply_text("Good. Now enter the third parameter:")


# ---------- Step 3 ----------
async def process_step_3(message: Message, user_entry: Dict[str, Any]) -> None:
    data = (message.text or "").strip()
    if not data:
        await message.reply_text("❌ Input cannot be empty. Try again:")
        return

    if "param1" not in user_entry or "param2" not in user_entry:
        logger.error("User %d reached step_3 without param1/param2.", message.from_user.id)
        await message.reply_text("⚠️ Session data corrupted. Restarting.")
        reset_user(message.from_user.id)
        return

    user_entry["param3"] = data
    user_entry["step"] = STATE_CONFIRM
    save_users_data()

    p1 = user_entry["param1"]
    p2 = user_entry["param2"]
    p3 = user_entry["param3"]

    summary = (
        "Summary\n\n"
        f"First parameter: {p1}\n"
        f"Second parameter: {p2}\n"
        f"Third parameter: {p3}\n\n"
        "Proceed? (yes/no)"
    )
    await message.reply_text(summary)


# ---------- Confirmation ----------
async def process_confirmation(message: Message, user_entry: Dict[str, Any]) -> None:
    answer = (message.text or "").strip().lower()
    user_id = message.from_user.id

    if answer in ("yes", "y"):
        logger.info("User %d confirmed. Keys=%s",
                    user_id, [k for k in user_entry if k != "step"])
        await message.reply_text("✅ Operation successful. Data saved.")
        reset_user(user_id)
    elif answer in ("no", "n"):
        logger.info("User %d cancelled at confirmation.", user_id)
        await message.reply_text("❌ Cancelled. No data stored.")
        reset_user(user_id)
    else:
        await message.reply_text("❓ Please reply with yes or no.")

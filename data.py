import json
import os
import logging
from pathlib import Path
from pyrogram.types import InlineKeyboardButton

# Import settings from config.py (OWNER_ID, LOG_GROUP_ID)
from config import OWNER_ID, LOG_GROUP_ID as LOGGER_GROUP_ID

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
#  File paths for atomic JSON persistence
# ---------------------------------------------------------------------------
DATA_FILE = Path("users_data.json")
TEMP_FILE = Path("users_data.json.tmp")

# ---------------------------------------------------------------------------
#  Bot commands (used in filters.command)
# ---------------------------------------------------------------------------
BOT_COMMANDS = ["start", "cancel", "broadcast", "stats"]

# ---------------------------------------------------------------------------
#  In‑memory state store
# ---------------------------------------------------------------------------
users_data: dict = {}


def save_users_data():
    """Atomically write current state to disk."""
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(users_data, f)
    os.replace(TEMP_FILE, DATA_FILE)


def load_users_data():
    """
    Restore state from disk.
    - Converts string keys back to int (JSON keys are always strings).
    - Handles corrupted file gracefully.
    """
    global users_data
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                raw = json.load(f)
            # JSON keys are strings → convert to int
            users_data = {int(k): v for k, v in raw.items()}
        except Exception:
            logger.exception("Corrupted users_data.json, starting fresh.")
            users_data = {}
    else:
        users_data = {}


# Load any existing state when the module is imported
load_users_data()


# ---------------------------------------------------------------------------
#  Your original Data class (untouched)
# ---------------------------------------------------------------------------
class Data:
    start_buttons = [
        [
            InlineKeyboardButton(
                "Generate Session",
                callback_data="generate"
            )
        ],
        [
            InlineKeyboardButton(
                "Updates",
                url="https://t.me/Nexaroid"
            ),
            InlineKeyboardButton(
                "Promotion",
                url="https://t.me/GenZpromo"
            )
        ],
        [
            InlineKeyboardButton(
                "Owner",
                url="https://t.me/dhruvOrigin"
            )
        ]
    ]

    generate_buttons = [
        [
            InlineKeyboardButton(
                "Pyrogram",
                callback_data="pyrogram"
            ),
            InlineKeyboardButton(
                "Telethon",
                callback_data="telethon"
            )
        ],
        [
            InlineKeyboardButton(
                "Home",
                callback_data="home"
            )
        ]
    ]

    pyrogram_buttons = [
        [
            InlineKeyboardButton(
                "V2",
                callback_data="pyrogram_v2"
            ),
            InlineKeyboardButton(
                "V3",
                callback_data="pyrogram_v3"
            )
        ],
        [
            InlineKeyboardButton(
                "Back",
                callback_data="generate"
            )
        ],
        [
            InlineKeyboardButton(
                "Home",
                callback_data="home"
            )
        ]
    ]

    telethon_buttons = [
        [
            InlineKeyboardButton(
                "V2",
                callback_data="telethon_v2"
            ),
            InlineKeyboardButton(
                "V3",
                callback_data="telethon_v3"
            )
        ],
        [
            InlineKeyboardButton(
                "Back",
                callback_data="generate"
            )
        ],
        [
            InlineKeyboardButton(
                "Home",
                callback_data="home"
            )
        ]
    ]

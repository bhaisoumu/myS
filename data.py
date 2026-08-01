from pyrogram.types import InlineKeyboardButton


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

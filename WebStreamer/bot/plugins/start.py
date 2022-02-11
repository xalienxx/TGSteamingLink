# (c) @EverythingSuckz | @Fmk

import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Contact my [Dev](https://t.me/TeamNezuko).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Devs](https://t.me/TeamNezuko).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text='Hi!!\nI am Instant Telegram File to Link Generator Bot.Please check /help options.\n\nSend/forward to me any file & \nsee the magic!🔮\n\nFor Start streaming server use /startbot command \n\nMaintenance by @XHunterK 🦅 @TeamNezuko 🇱🇰',
             reply_markup=InlineKeyboardMarkup(
                 [
                     [InlineKeyboardButton('📌 Devs Channel', url='https://t.me/TeamNezuko')], #InlineKeyboardButton('Support Group', url='https://t.me/*****')],
                     [InlineKeyboardButton('📌 Mikasa 2.0 Project', url='https://t.me/TeamNezuko/62')]
                 ]
             ),
             disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry Bruh, You are Banned to use me. Contact my [Devs](https://t.me/TeamNezuko).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh / Try Again",
                                                     url=f"https://t.me/{(await b.get_me()).username}?start=*********_{usr_cmd}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Devs](https://t.me/TeamNezuko).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.message_id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id,
                                     file_name)

        msg_text = "Hey! Your Link Generated!📎 \n\n**File Name:** `{}`\n**File Size:** `{}`\n\n**Download Link:** `{}`"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Now!", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Contact my [Devs](https://t.me/TeamNezuko).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Something went Wrong. Contact my [Devs](https://t.me/TeamNezuko).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="Send/Forward to me any File I will provide External Direct Download Link!\n\nCheck bot status : https://cutt.ly/JIY88jo [Password: Mikasa]",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        #reply_markup=InlineKeyboardMarkup(
            #[
                #[InlineKeyboardButton("Support Group", url="https://t.me/JoinOT"), #InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")],
                #[InlineKeyboardButton("Developer", url="https://t.me/TeamNezuko")]
            #]
        #)
    )

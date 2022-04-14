# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """


import os
import re
import requests
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from math import ceil
from platform import python_version


from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from telethon import version
from telethon.sync import TelegramClient, custom, events
from telethon.sessions import StringSession


# For Download config.env
CONFIG_FILE_URL = os.environ.get("CONFIG_FILE_URL", None)
if CONFIG_FILE_URL is not None:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
    log = getLogger(__name__)
    try:
        res = requests.get(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open("config.env", "wb") as f:
                f.write(res.content)
        else:
            log.error(f"Failed to load config.env {res.status_code}")
            quit(1)
    except Exception as e:
        log.error(str(e))
        quit(1)


load_dotenv("config.env")

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE") or "False")

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = (os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)

# Telegram App KEY and HASH
API_KEY = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# =====================================================================
SUDO_USERS = {
    int(x) for x in os.environ.get(
        "SUDO_USERS",
        "").split()}
BL_CHAT = {int(x) for x in os.environ.get("BL_CHAT", "").split()}
# =====================================================================

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", 0))

BOT_VER = "0.1.0"

HANDLER = os.environ.get("HANDLER") or "."
SUDO_HANDLER = os.environ.get("SUDO_HANDLER") or "$"

# Userbot logging feature switch.
LOGSPAMMER = sb(
    os.environ.get(
        "LOGSPAMMER",
        "False")) if BOTLOG_CHATID else False
# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

# Github Credentials for updater and Gitupload.
GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)

# Genius lyrics get this value from https://genius.com/developers both has
# same values
GENIUS = os.environ.get("GENIUS_API_TOKEN", None)

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL", "https://github.com/farizjs/FlicksProject")
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "sql-extended")

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get(
    "CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", None)

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/usr/bin/chromedriver")
GOOGLE_CHROME_BIN = os.environ.get(
    "GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Default .alive name
ALIVE_NAME = os.environ.get("ALIVE_NAME", "glx")

# Default .alive logo
ALIVE_LOGO = os.environ.get("ALIVE_LOGO", "https://telegra.ph/file/a61b3065d139ef6d620f1.jpg")

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY", "id"))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", "404 Not Found")
LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API is not None:
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA", None)
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
    "TMP_DOWNLOAD_DIRECTORY", "./downloads/")

# Terminal alias
TERM_ALIAS = os.environ.get("TERM_ALIAS", "Galaxy")

# Zipfile module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

# Deezloader
DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN", None)

# Inline bot helper
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)


# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)



# Global Variables
CMD_LIST = {}
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
LOAD_PLUG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 2
    global lockpage
    lockpage = page_number
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline(
            "{} {} ✘".format(
                "✘", x), data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols],
                     modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "««", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "Cʟᴏsᴇ", data="{}_close({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "»»", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs

with bot:
    try:

        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH).start(
            bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id
        main_help_button = [
            [
                Button.url("Settings ⚙️", f"t.me/{BOT_USERNAME}?start=set"),
                Button.inline("Vc Menu ⚙️", data="galaxy_inline"),
            ],
            [
                Button.inline("Help Menu", data="open"),
                Button.inline("Owner Menu", data="ownrmn"),
            ],
            [Button.inline("Close", data="close")],
        ]


        @tgbot.on(events.NewMessage(pattern="/start"))
        async def handler(event):
            if event.message.from_id != uid:
                await event.reply("Hey there!, this is Galaxy Assistant of {ALIVE_NAME}!\n\n you can chat {ALIVE_NAME} with me!")
            else:
                await event.reply(f"Hey there {ALIVE_NAME}\n\nI work for you :)")

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"get_back")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                current_page_number = int(lockpage)
                buttons = paginate_help(current_page_number, plugins, "helpme")
                text = f"\n📚 **Inline Help Menu!**\n\n **Master​** {ALIVE_NAME}\n\n** Branch :** Galaxy-Userbot\n** ᴠᴇʀsɪᴏɴ :** `v{BOT_VER}`\n** Plugins :** `{len(plugins)}`\n"
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = f"You are Not allowed, this Userbot Belongs {ALIVE_NAME}"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"open")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                buttons = paginate_help(0, plugins, "helpme")
                text = f"\n📚 **Inline Help Menu!**\n\n **Master​** {ALIVE_NAME}\n\n** Branch :** Galaxy-Userbot\n** ᴠᴇʀsɪᴏɴ :** `v{BOT_VER}`\n** Plugins :** `{len(plugins)}`\n"
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = f"You are Not allowed, this Userbot Belongs {ALIVE_NAME}"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("galaxyo"):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.photo(
                    file=ALIVE_LOGO,
                    link_preview=False,
                    text=f"\n**Galazy-Userbot**\n\n✥**Mᴀsᴛᴇʀ​** {ALIVE_NAME}\n\n✥**ʙʀᴀɴᴄʜ :** Galaxy-Userbot\n✥**ᴠᴇʀsɪᴏɴ :** {BOT_VER}\n✥**Plugins** : {len(plugins)}".format(
                        len(dugmeler),
                    ),
                    buttons=main_help_button,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "UserButt Helper",
                    text="List of Modules",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    "Galaxy Userbot",
                    text="""You can convert your account to bot and use them. Remember, you can't manage someone else's bot! All installation details are explained from GitHub address below.""",
                    buttons=[
                        [
                            custom.Button.url(
                                "GitHub Repo",
                                "https://github.com/farizjs/Galaxy-Userbot"),
                            custom.Button.url(
                                "Support",
                                "https://t.me/FlicksSupport")],
                    ],
                    link_preview=False,
                )
            await event.answer([result] if result else None)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_close\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # @Flicasyncks_Userbot
                # https://t.me/TelethonChat/115200
                text = (
                    f"\n**Usᴇʀʙᴏᴛ Tᴇʟᴇɢʀᴀᴍ**\n\n **Mᴀsᴛᴇʀ** {ALIVE_NAME}\n\n** Bʀᴀɴᴄʜ :** Galaxy-Userbot\n** Vᴇʀsɪ :** `v{BOT_VER}`\n** Pʟᴜɢɪɴs :** `{len(plugins)}`\n")
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    link_preview=True,
                    buttons=main_help_button)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"gcback")
            )
        )
        async def gback_handler(event):
            if event.query.user_id == uid:  # @Flicasyncks_Userbot
                # https://t.me/TelethonChat/115200
                text = (
                    f"\n**Usᴇʀʙᴏᴛ Tᴇʟᴇɢʀᴀᴍ**\n\n **Mᴀsᴛᴇʀ** {ALIVE_NAME}\n\n** Bʀᴀɴᴄʜ :** Galaxy-Userbot\n** Vᴇʀsɪ :** `v{BOT_VER}`\n** Pʟᴜɢɪɴs :** `{len(plugins)}`\n")
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    link_preview=True,
                    buttons=main_help_button)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"ownrmn")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                text = (
                    f"Owner menu for {ALIVE_NAME} \n"
                    f"`Branch    :` {UPSTREAM_REPO_BRANCH} \n"
                    f"`Versi Bot :` {BOT_VER} \n"
                    f"`Plugins   :` {len(plugins)} \n"
                    f"`Bahasa    :` Python \n"
                    f"`Database  :` SQL \n")
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    link_preview=True,
                    buttons=[
                        [
                            Button.inline("Ping ⚡",
                                          data="pingbot"),
                            Button.inline("About ?",
                                          data="about")],
                        [custom.Button.inline(
                            "Back", data="gcback")],
                    ]
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"pingbot")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                start = datetime.now()
                end = datetime.now()
                ms = (end - start).microseconds / 1000
                await event.answer(
                    f"PONG 🏓\n {ms}ms", cache_time=0, alert=True)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.CallbackQuery(data=b"about"))
        async def about(event):
            if event.query.user_id == uid:
                await event.edit(f"""
Owner - {ALIVE_NAME}
OwnerID - {uid}
[Link To Profile 👤](tg://user?id={uid})
Owner repo - [Fariz](tg://openmessage?user_id=1514078508)
Support - @FlicksSupport
Galaxy-Userbot [v{BOT_VER}](https://github.com/farizjs/Galaxy-Userbot)
""",
                                 buttons=[
                                     [
                                         Button.url("Repo",
                                                    "https://github.com/farizjs/Galaxy-Userbot"),
                                         custom.Button.inline("ʙᴀᴄᴋ​",
                                                              data="ownrmn")],
                                 ]
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.CallbackQuery(data=b"galaxy_inline"))
        async def about(event):
            if event.query.user_id == uid:
                await event.edit(f"""
Voice chat group menu for {ALIVE_NAME}
""",
                                 buttons=[
                                     [
                                         Button.inline("Vc Plugin ⚙️",
                                                       data="vcplugin"),
                                         Button.inline("Vc Tools ⚙️",
                                                       data="vctools")],
                                     [custom.Button.inline(
                                         "Back", data="gcback")],
                                 ]
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"vcplugin")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                text = (
                    """
Command: .play <song title / link yt>
Usage: To play songs on Voice Chat Group with your account

Command: .vplay <video title / YT link>
Usage: To play videos on Voice Chat Group with your account

Command: .end
Usage: To stop the video / song that is playing at Voice Chat Group

Command: .skip
Usage: To pass videos / songs that are being played

Command: .pause
Usage: To stop the video / song that is playing

Command: .resume
Usage: To continue playing videos / songs that are playing

Command: .volume 1-200
Usage: To change the volume (requires admin rights)

Command: .playlist
Usage: To display playlists of songs / videos
""")
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    link_preview=True,
                    buttons=[Button.inline("Back", data="galaxy_inline")])
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"vctools")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                text = (
                    """
Plugin: VcTools.

Command: .startvc
Usage: to start voice chat group

Command: .stopvc
Usage: To stop Voice Chat Group

Command: .vctitle <title VCG>
Usage: To change the title / title Voice Chat Group

Command: .vcinvite.
Usage: invite member group to Voice Chat Group

Command: .joinvc
Usage: for JOIN VC Group

Command: .leavevc
Usage: To get off VC Group
""")
                await event.edit(
                    text,
                    file=ALIVE_LOGO,
                    link_preview=True,
                    buttons=[Button.inline("Back", data="galaxy_inline")])
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.CallbackQuery(data=b"close"))
        async def close(event):
            if event.query.user_id == uid:
                buttons = [
                    (custom.Button.inline("Open Menu", data="gcback"),),
                ]
                await event.edit("**Menu is closed​!**", file=ALIVE_LOGO, buttons=buttons)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nYou have no right to press these buttons"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 999:
                    help_string = (
                        str(CMD_HELP[modul_name])[:999] + "..."
                        + "\n\nRead more .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name])

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} No document has been written for module.".format(
                        modul_name
                    )
                )
                await event.edit(
                    reply_pop_up_alert, buttons=[
                        Button.inline("Back", data="get_back")]
                )

            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGS.info(
            "Support for inline is disabled on your bot. "
            "To enable it, define a bot token and enable inline mode on your bot. "
            "If you think there is a problem other than this, contact us.")


from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import *

import logging
from datetime import datetime
import os

# Setup logging and fallback config values
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", 10))

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={{"root": "plugins"}}
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL1:
            try:
                chat = await self.get_chat(FORCE_SUB_CHANNEL1)
                link = chat.invite_link
                if not link:
                    link = await self.export_chat_invite_link(FORCE_SUB_CHANNEL1)
            except Exception as e:
                self.LOGGER.error(f"Force sub channel invite link error: {{e}}")

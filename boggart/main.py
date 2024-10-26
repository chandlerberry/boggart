import asyncio
import asyncpg
import logging
import logging.handlers
import os
import sys
from typing import List
import discord
from discord.ext import commands

class Boggart(commands.Bot):
    def __init__(self, *args, initial_extensions: List[str], db_pool: asyncpg.Pool, **kwargs,):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.db_pool = db_pool
        self.command_prefix='!'
        self.logger = logging.getLogger('discord')

    async def setup_hook(self) -> None:
        """Load anything that should be in memory prior to handling events"""
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            self.logger.info(f'{extension} loaded')

async def main():
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')
    
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(stream_handler)

    pg_username = os.getenv('POSTGRES_USERNAME')
    pg_password = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('POSTGRES_HOST')

    async with asyncpg.create_pool(
        user=pg_username,
        password=pg_password,
        host=pg_host,
        port=5432,
        database='boggart',
        command_timeout=60
    ) as pool:

        exts = ['ImageGenerator']
        intents = discord.Intents.default()
        intents.message_content = True
        
        async with Boggart(commands.when_mentioned, db_pool=pool, initial_extensions=exts, intents=intents) as bot:
            await bot.start(os.getenv('DISCORD_BOT_KEY'))

asyncio.run(main())
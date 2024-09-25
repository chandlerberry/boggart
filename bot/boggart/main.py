import asyncio
import asyncpg
import logging
import logging.handlers
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

        # Load extensions prior to sync to ensure interactions defined in those extensions are synced as well
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            self.logger.info(f'{extension} loaded')

async def main():

    # todo: remove all this secret bs
    get_secret = lambda secret_file: open(f"/run/secrets/{secret_file}", 'r').read()

    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')
    
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(stream_handler)
    
    # todo: load env vars from dotenv library, and pass as kwargs to connection pool
    pg_user = get_secret('postgres_username')
    pg_pass = get_secret('postgres_password')
    pg_host = get_secret('postgres_host')
    pg_port = get_secret('postgres_port')
    pg_database = get_secret('postgres_database')

    async with asyncpg.create_pool(user=pg_user, password=pg_pass, host=pg_host, port=pg_port, database=pg_database, command_timeout=60) as pool:
        
        exts = ['ImageGenerator']
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        async with Boggart(commands.when_mentioned, db_pool=pool, initial_extensions=exts, intents=intents) as bot:
            await bot.start(get_secret('discord_bot_key'))

asyncio.run(main())
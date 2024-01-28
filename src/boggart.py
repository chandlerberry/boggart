import asyncio
import asyncpg
import logging
import logging.handlers
import sys
from typing import List #, Optional
import discord
from discord.ext import commands
# from aiohttp import ClientSession

class Boggart(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        # web_client: ClientSession,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # self.web_client = web_client
        self.initial_extensions = initial_extensions
        self.db_pool = db_pool
        self.command_prefix='!'
        self.logger = logging.getLogger('discord')
        self.pg_logger = logging.getLogger('discordgpt.postgres')

    async def setup_hook(self) -> None:
        """
        Load anything that should be in memory prior to handling events
        """
        # Load extensions prior to sync to ensure interactions defined in those extensions are synced as well
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            self.logger.info(f'{extension} loaded')

async def main():
    get_secret = lambda secret_file: open(f"/run/secrets/{secret_file}", 'r').read()

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')
    stream_handler.setFormatter(formatter)

    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(stream_handler)

    pg_logger = logging.getLogger('discordgpt.postgres')
    pg_logger.setLevel(logging.INFO)
    pg_logger.addHandler(stream_handler)
    pg_user = get_secret('postgres_username')
    pg_pass = get_secret('postgres_password')
    pg_host = get_secret('postgres_host')
    pg_port = get_secret('postgres_port')
    pg_database = get_secret('postgres_database')
    # pg_dsn = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_database}'

    # async with ClientSession() as boggart_client, asyncpg.create_pool(dsn=pg_dsn, command_timeout=60) as pool:
    async with asyncpg.create_pool(
        user=pg_user,
        password=pg_pass,
        host=pg_host,
        port=pg_port,
        database=pg_database,
        command_timeout=60
    ) as pool:
        exts = ['discordgpt.ImageGenerator']
        intents = discord.Intents.default()
        intents.message_content = True
        async with Boggart(
            commands.when_mentioned,
            db_pool=pool,
            initial_extensions=exts,
            intents=intents,
        ) as bot:
            await bot.start(get_secret('discord_bot_key'))

asyncio.run(main())
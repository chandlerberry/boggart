import asyncio
import logging
import logging.handlers
import os
import sys
import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine
from boggart.core import Boggart


async def main():
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", date_format, style="{"
    )

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(stream_handler)

    pg_engine = create_async_engine(os.getenv("PG_CONNECTION"))
    exts = ["image_generator"]
    intents = discord.Intents.default()
    intents.message_content = True

    async with Boggart(
        commands.when_mentioned,
        pg_engine=pg_engine,
        initial_extensions=exts,
        intents=intents,
    ) as bot:
        await bot.start(os.getenv("DISCORD_BOT_KEY"))


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import discord
import os
from discordgpt import KeyLoader
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load_cogs():
    await bot.load_extension('discordgpt.ImageGenerator')

@bot.event
async def on_ready():
    print("\nBoggart Connected\n")

async def main():
    keys = KeyLoader(keys_file='/config/staging.yaml',
                    schema_file='/config/schema.json')

    os.environ["OPENAI_API_KEY"] = keys.openai
    os.environ["AWS_ENDPOINT_URL"] = keys.backblaze["endpoint_url"]
    os.environ["AWS_ACCESS_KEY_ID"] = keys.backblaze["application_key_id"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = keys.backblaze["application_key"]

    await load_cogs()
    await bot.start(keys.discord)

asyncio.run(main())
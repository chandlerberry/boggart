import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load_cogs():
    await bot.load_extension('discordgpt.ImageGenerator')

@bot.event
async def on_ready():
    print("\nBoggart Connected\n")

async def main():
    get_secret = lambda secret_file: open(f"/run/secrets/{secret_file}", 'r').read()
    await load_cogs()
    await bot.start(get_secret('discord_bot_key'))

asyncio.run(main())
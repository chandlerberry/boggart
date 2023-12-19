import asyncio
import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load_cogs():
    await bot.load_extension('discordgpt.ImageGenerator')

@bot.event
async def on_ready():
    print("\nBoggart Connected\n")

async def main():
    await load_cogs()
    await bot.start(os.getenv('DISCORD_BOT_KEY'))

asyncio.run(main())
import asyncio
import discord
from discordgpt import KeyLoader
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load_cogs():
    await bot.load_extension('discordgpt.ImageGenerator')

@bot.event
async def on_ready():
    print("\nBoggart Connected\n")

async def main():
    keys = KeyLoader('keys.json')
    await load_cogs()
    await bot.start(keys.discordBot)

asyncio.run(main())
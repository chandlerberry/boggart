import asyncio
import discord
import os
from discordgpt import KeyLoader
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# "Cogs" are weird and I wish I could do this differently, but here we are
async def load_cogs():
    await bot.load_extension('discordgpt.ImageGenerator')

@bot.event
async def on_ready():
    print("\nBoggart Connected\n")

async def main():
    keys = KeyLoader(keys_file="keys.yaml",schema_file="schema.json")
    os.environ.update(keys["backblaze"])
    await load_cogs()
    await bot.start(keys.discordBot)

asyncio.run(main())
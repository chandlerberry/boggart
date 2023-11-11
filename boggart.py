import asyncio
import discord
from discordgpt import KeyLoader, ImageGenerator
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("\nBOGGART CONNECTED\n")

async def main():
    keys = KeyLoader('keys.json')
    bot.start(keys.discordBot)
    bot.add_cog(ImageGenerator(bot,
                               api_key=keys.openai,
                               model='dall-e-3',
                               resolution='1024x1024'))

asyncio.run(main())
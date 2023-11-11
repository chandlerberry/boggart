import discord
from discord.ext import commands
from access import ApiKeyLoader
from discordgpt import ImageGenerator

keys = ApiKeyLoader('keys.json', 'schema.json')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event  
async def on_ready():
    print("\nBOGGART CONNECTED\n")

bot.run(keys.discord)
bot.add_cog(ImageGenerator(bot))
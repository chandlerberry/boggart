import asyncio
import aiohttp
import discord
import io
from discord.ext import commands
from openai import OpenAI
from discordgpt import KeyLoader

class ImageGenerator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def img_test(self, ctx):
        await ctx.send('hello')

    async def generate_image(self, prompt):
        keys = KeyLoader('keys.json')
        client = OpenAI(
            api_key=str(keys.openai)
        )
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard",
        )
        print(f"\n{result.data[0].revised_prompt}\n")
        return result.data[0].url
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("DiscordGPT Image Generator Ready\n")

    @commands.command()
    async def img(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart':
            return
        await ctx.send(f"Generating: \"{prompt}\"")
        try:
            image_url = await self.generate_image(prompt)
        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status != 200:
                        await ctx.send("Failed to download the image.")
                        return
                    
                    image_data = await response.read()
                    image = io.BytesIO(image_data)
                    filename = f"{ctx.message.author.display_name}.png"

                    await ctx.send(file=discord.File(fp=image, filename=filename))

        except Exception as e:
            await ctx.send(f"Error sending image: {e}")

async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
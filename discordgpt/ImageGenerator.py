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

    async def generate_image(self, prompt, image_size, image_quality):
        keys = KeyLoader('keys.json')
        client = OpenAI(
            api_key=str(keys.openai)
        )
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=image_size,
            quality=image_quality,
        )
        return result
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("DiscordGPT Image Generator Ready\n")

    @commands.command()
    async def img(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart':
            return
        await ctx.send(f"Generating: \"{prompt}\"")
        try:
            image_result = await self.generate_image(prompt, '1024x1024', 'standard')
        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_result.data[0].url) as response:
                    if response.status != 200:
                        await ctx.send("Failed to download the image.")
                        return
                    
                    image_data = await response.read()
                    image = io.BytesIO(image_data)
                    filename = f"{ctx.message.author.display_name}.png"

                    await ctx.send(image_result.data[0].revised_prompt, file=discord.File(fp=image, filename=filename))

        except Exception as e:
            await ctx.send(f"Error sending image: {e}")

    @commands.command()
    async def img_hd(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart' and str(ctx.message.author) != 'chndlr':
            await ctx.send("Tell CHBE he needs more money")
            return
        await ctx.send(f"Generating HD Image: \"{prompt}\"")
        try:
            image_result = await self.generate_image(prompt, '1792x1024', 'hd')

        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_result.data[0].url) as response:
                    if response.status != 200:
                        await ctx.send("Failed to download the image.")
                        return
                    
                    image_data = await response.read()
                    image = io.BytesIO(image_data)
                    filename = f"{ctx.message.author.display_name}.png"

                    await ctx.send(image_result.data[0].revised_prompt, file=discord.File(fp=image, filename=filename))

        except Exception as e:
            await ctx.send(f"Error sending image: {e}")

async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
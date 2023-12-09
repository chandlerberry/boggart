import aiohttp
import boto3
import discord
import io
from discord.ext import commands
from openai import OpenAI

class ImageGenerator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def generate_image(self, **kwargs: str):
        prompt = kwargs.get('prompt')
        image_size = kwargs.get('image_size')
        image_quality = kwargs.get('image_quality')
        client = OpenAI()
        result = client.images.generate(model=self.dalle_model,
                                        prompt=prompt,
                                        n=1, size=image_size,
                                        quality=image_quality)
        return result

    async def download_image(self, ctx, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    # I want to handle this differently eventually so as to not have to pass the context to the function
                    await ctx.send("Failed to download the image.")
                    return
                image_data = await response.read()
                return io.BytesIO(image_data)
    
    # get url of uploaded image, store reference in sql database
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#s3
    async def store_image(self, image_data: io.BytesIO, image_name: str, bucket_name: str) -> str:
        b2_client = boto3.client('s3')
        b2_client.put_object(Bucket=bucket_name,
                             Key=image_name,
                             Body=image_data)
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("DiscordGPT Image Generator Ready\n")

    @commands.command()
    async def img(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart':
            return
        await ctx.send(f"Generating: \"{prompt}\"")

        try:
            image_result = await self.generate_image(prompt=str(prompt),
                                                     image_size='1024x1024',
                                                     image_quality='standard')

        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return
        
        try:
            image = await self.download_image(ctx, image_result.data[0].url)
            filename = f"{ctx.message.author.display_name}.png"
            await ctx.send(image_result.data[0].revised_prompt,
                           file=discord.File(fp=image, filename=filename))
            
        except Exception as e:
            await ctx.send(f"Error sending image: {e}")

    @commands.command()
    async def img_hd(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart':
            return
        await ctx.send(f"Generating HD Image: \"{prompt}\"")

        try:
            image_result = await self.generate_image(prompt=str(prompt),
                                                     image_size='1792x1024',
                                                     image_quality='hd')

        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return

        try:
            filename = f"{ctx.message.author.display_name}.png"
            image = await self.download_image(ctx, image_result.data[0].url)
            await ctx.send(image_result.data[0].revised_prompt,
                           file=discord.File(fp=image, filename=filename))

        except Exception as e:
            await ctx.send(f"Error sending image: {e}")

async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
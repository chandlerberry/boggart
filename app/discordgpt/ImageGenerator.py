import aiohttp
import asyncio
import boto3
import discord
import io
import os
import uuid
from discord.ext import commands
from openai import OpenAI
from botocore.exceptions import NoCredentialsError

class ImageGenerator(commands.Cog):
    """
    Discord.py Cog for generating images using OpenAI DALLE
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # I dislike "Cogs", requires lazy import here to avoid dependency loops. If I were able to instantiate this class by simply importing it in 'boggart.py' I would be using dependency injection
        from .Database import ImageDatabase
        self.db = ImageDatabase(pg_username='postgres',
                                pg_password='chandlerb',
                                pg_db='postgres',
                                host='127.0.0.1:5432')

    async def generate_image(self, **kwargs: str):
        """
        Generates an image result from the provided prompt using the OpenAI API `client.images.generate()`.
        """
        prompt = kwargs.get('prompt')
        image_size = kwargs.get('image_size')
        image_quality = kwargs.get('image_quality')

        client = OpenAI()
        result = client.images.generate(model=os.getenv('DALLE_MODEL'),
                                        prompt=prompt,
                                        n=1, size=image_size,
                                        quality=image_quality)
        return result

    async def download_image(self, ctx, url) -> io.BytesIO:
        """
        Download the `.png` image generated by OpenAI API using the temporary link provided. Returns type `io.BytesIO` if successful.

        Arguments:
        - `ctx`: Discord message context
        - `url`: Temporary URL provided by OpenAI API call
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("Failed to download the image.")
                    return
                image_data = await response.read()
                return io.BytesIO(image_data)
            
    async def send_image(self, ctx, lock: asyncio.Lock, image_data: io.BytesIO, filename: str, caption: str):
        """
        Send Image to Discord chat
        """
        async with lock:
            await ctx.send(caption, file=discord.File(fp=image_data, filename=filename))
            # TODO: log that the chat was sent
    
    async def upload_generated_image(self, lock: asyncio.Lock, image_data: io.BytesIO, b2_filename: str, bucket_name='boggart'):
        """
        Upload generated image to object storage using the `boto3` AWS API.
        
        Arguments:
        - `lock`: asyncio.Lock type for thread-safe handling of `image_data`
        - `image_data`: The image data as a `io.BytesIO` object
        - `image_name`: Filename of the uploaded image
        - `bucket_name`: Name of storage bucket being 
        """
        async with lock:
            image_data.seek(0)
            try:
                b2 = boto3.client('s3')
                b2.put_object(Bucket=bucket_name,
                              Key=b2_filename,
                              Body=image_data)

            except NoCredentialsError as e:
                print("Credentials not available")
            
    @commands.Cog.listener()
    async def on_ready(self):
        """
        Logs that the ImageGenerator "Cog" is Online
        """
        print("DiscordGPT Image Generator Ready\n")

    @commands.command()
    async def img(self, ctx, *, prompt):
        """
        Chat command for user to generate a 1024x1024 image using DALLE 3 Standard.
        """
        # TODO: set channel as environment variable for container
        if str(ctx.message.channel) != 'boggart-2':
            return
        
        filename = f"{uuid.uuid4().hex}.png"
        
        # TODO: log that image request was recieved by 'x' user

        try:
            image_result = await self.generate_image(prompt=str(prompt),
                                                     image_size='1024x1024',
                                                     image_quality='standard')
            
        except Exception as e:
            await ctx.send(f"Error generating image: {e}")
            return
        
        try:
            image = await self.download_image(ctx, image_result.data[0].url)

        except Exception as e:
            await ctx.send(f"Error downloading image: {e}")
            return
        
        lock = asyncio.Lock()

        try:
            # send to discord chat
            send = asyncio.create_task(self.send_image(ctx,
                                                       lock,
                                                       image_data=image,
                                                       filename=filename,
                                                       caption=image_result.data[0].revised_prompt))
            # upload to backblaze
            upload = asyncio.create_task(self.upload_generated_image(lock,
                                                                     image_data=image,
                                                                     b2_filename=filename,
                                                                     bucket_name='boggart'))
            # store reference to file in database
            store = asyncio.create_task(self.db.store_generated_image(b2_filename=filename,
                                                                      username=ctx.message.author.display_name,
                                                                      prompt=prompt,
                                                                      caption=image_result.data[0].revised_prompt))
            
            await asyncio.gather(send, upload, store)
                
        except Exception as e:
            await ctx.send(f"Error sending/storing image: {e}")
            return

async def setup(bot):
    """
    Required to load the image generator cog when the service starts
    """
    await bot.add_cog(ImageGenerator(bot))
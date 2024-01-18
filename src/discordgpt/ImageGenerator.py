import asyncio
import boto3
import discord
import io
import logging
import os
import sys
import uuid
from aiohttp import ClientSession
from discord.ext import commands
from openai import OpenAI
from botocore.exceptions import NoCredentialsError

class ImageGenerator(commands.Cog):
    """
    Discord.py Cog for generating images using OpenAI DALLE
    """
    def __init__(self, bot):
        self.bot = bot
        self.get_secret = lambda secret_file: open(f"/run/secrets/{secret_file}", 'r').read()
        self.lock = asyncio.Lock()

        self.stream_handler = logging.StreamHandler(stream=sys.stdout)
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', self.date_format, style='{')
        self.stream_handler.setFormatter(self.formatter)

        self.img_logger = logging.getLogger('discordgpt.imagegenerator')
        self.img_logger.setLevel(logging.INFO)
        self.img_logger.addHandler(self.stream_handler)

        os.environ['AWS_ENDPOINT_URL'] = self.get_secret('backblaze_endpoint_url')
        os.environ['AWS_ACCESS_KEY_ID'] = self.get_secret('backblaze_application_key_id')
        os.environ['AWS_SECRET_ACCESS_KEY'] = self.get_secret('backblaze_application_key')

    async def __generate_image(self, **kwargs: str):
        """
        Generates an image result from the provided prompt using the OpenAI API `client.images.generate()`
        """
        prompt = kwargs.get('prompt')
        image_size = kwargs.get('image_size')
        image_quality = kwargs.get('image_quality')

        client = OpenAI(api_key=self.get_secret('openai_api_key'))
        result = client.images.generate(
            model=self.get_secret('openai_dalle_model'),
            prompt=prompt,
            n=1, size=image_size,
            quality=image_quality
        )
        
        self.img_logger.info('Image downloaded from OpenAI')
        return result

    async def __download_image(self, ctx, url) -> io.BytesIO:
        """
        Download the `.png` image generated by OpenAI API using the temporary link provided.
        Returns type `io.BytesIO` if successful.

        Arguments:
        - `ctx`: Discord message context
        - `url`: Temporary URL provided by OpenAI API call
        """
        async with ClientSession() as session, session.get(url) as response:
            if response.status != 200:
                await ctx.send('Failed to download the image.')
                self.img_logger.warning('Could not download image from OpenAI')
                return
            
            image_data = await response.read()
            return io.BytesIO(image_data)
            
    async def __send_image(
            self,
            ctx,
            image_data: io.BytesIO,
            filename: str,
            caption: str
        ):
        """
        Send Image to Discord chat
        """
        self.img_logger.info(f'Sending image {filename} to Discord')
        async with self.lock:
            image_data.seek(0)
            await ctx.send(
                caption,
                file=discord.File(fp=image_data, filename=filename)
            )
    
    async def __upload_generated_image(
            self,
            image_data: io.BytesIO,
            b2_filename: str,
            bucket_name: str
        ):
        """
        Upload generated image to object storage using the `boto3` package
        """
        self.img_logger.info(f'Uploading image {b2_filename} to Backblaze')
        async with self.lock:
            image_data.seek(0)
            try:
                b2 = boto3.client('s3')
                b2.put_object(
                    Bucket=bucket_name,
                    Key=b2_filename,
                    Body=image_data
                )

            except NoCredentialsError as e:
                self.img_logger.error(f'Issue with Backblaze Credentials: {e}')

    @commands.command()
    async def img(self, ctx, *, prompt):
        """
        Chat command for a user to generate an image using DALLE 3 Standard.
        """
        if str(ctx.message.channel) != self.get_secret('discord_image_channel'):
            return
        
        await ctx.send(f'Generating...')
        self.img_logger.info(f'Image request recieved from {ctx.message.author.display_name}')
        
        filename = f"{uuid.uuid4().hex}.png"
        link = f"https://boggart.s3.us-east-005.backblazeb2.com/{filename}"

        try:
            image_result = await self.__generate_image(
                prompt=str(prompt),
                image_size=self.get_secret('openai_dalle_image_size'),
                image_quality=self.get_secret('openai_dalle_image_quality')
            )

        except Exception as e:
            await ctx.send(f'Error generating image: {e}')
            self.img_logger.error(f'Error generating image for {ctx.message.author.display_name}: {e}')
            return
        
        try:
            image = await self.__download_image(ctx, image_result.data[0].url)

        except Exception as e:
            await ctx.send(f"Error downloading image: {e}")
            self.img_logger.error(f"Could not download image: {e}")
            return

        try:
            async with asyncio.TaskGroup() as sus:
                # send to discord chat
                sus.send = asyncio.create_task(
                    self.__send_image(
                        ctx, 
                        image_data=image, 
                        filename=filename, 
                        caption=image_result.data[0].revised_prompt
                    )
                )

                # upload to backblaze
                sus.upload = asyncio.create_task(
                    self.__upload_generated_image( 
                        image_data=image,
                        b2_filename=filename, 
                        bucket_name=self.get_secret('backblaze_bucket_name')
                    )
                )

                # store reference to file in database
                sus.store = asyncio.create_task(
                    self.bot.store_generated_image(
                        b2_filename=filename, 
                        b2_link=link, 
                        username=ctx.message.author.display_name, 
                        prompt=prompt, 
                        caption=image_result.data[0].revised_prompt
                    )
                )
                
        except Exception as e:
            await ctx.send(f"Error sending/storing image: {e}")
            self.img_logger.error(f"Issue sending/storing image: {e}")
            return

async def setup(bot):
    """
    Required to load the image generator cog when the service starts
    """
    await bot.add_cog(ImageGenerator(bot))
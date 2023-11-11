import asyncio
import aiohttp
import discord
import io
import openai
from discord.ext import commands
from openai import OpenAI

class ImageGenerator(commands.Cog):
    def __init__(self, bot, api_key, model, resolution):
        self.bot = bot
        self.model = model
        self.resolution = resolution
        self.client = OpenAI(api_key)

    @commands.Cog.listener()
    async def on_ready():
        print("ImageGenerator ready")

    async def generate_image(self, prompt):
        result = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            n=1,
            size=self.resolution,
            quality="standard",
        )
        try:
            image_url = result.data[0].url
            revised_prompt = result.data[0].revised_prompt
        except openai.OpenAIError as e:
            return e.error
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as get:
                if get.status != 200:
                    return None
                return io.BytesIO(await get.read()), revised_prompt

    @commands.command()
    async def img(self, ctx, *, prompt):
        if str(ctx.message.channel) != 'boggart':
            return
        await ctx.send(f"Generating: \"{prompt}\"")
        # summary_thread = asyncio.to_thread(summarize_prompt(prompt))
        image_task = asyncio.to_thread(self.generate_image(prompt))
        image, revised_prompt = await image_task

        try:
            await ctx.send(f"{revised_prompt}", file=discord.File(fp=image, filename=f'By {ctx.message.author}.png'))
        except:
            await ctx.send("somethings broke")
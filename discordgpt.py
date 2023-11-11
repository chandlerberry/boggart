import asyncio
import aiohttp
import discord
import io
import openai
from openai import OpenAI
from discord.ext import commands
from access import ApiKeyLoader

class ImageGenerator(commands.Cog):
    def __init__(self, bot, model, resolution):
        self.bot = bot
        self.model = model
        self.resolution=resolution

    @commands.Cog.listener()
    async def on_ready():
        print("ImageGenerator ready")

    async def setup (bot):
        await bot.add_cog(ImageGenerator(bot))

    async def get_image(self, prompt):
        keys = ApiKeyLoader('keys.json', 'schema.json')
        client = OpenAI(api_key=keys.openai)
        result = client.images.generate(
            model=self.model,
            prompt=prompt,
            n=1,
            size=self.resolution,
            quality="standard",
        )
        print(result)
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
        image_task = asyncio.create_task(self.get_image(prompt))
        image, revised_prompt = await image_task

        try:
            await ctx.send(revised_prompt, file=discord.File(fp=image, filename=f'dalle.png'))
        except:
            await ctx.send("somethings broke")
        
        # if isinstance(image, str):
            # if "safety system" in image:
                # await ctx.send(f"\"{prompt}\" has been determined to be too based for the OpenAI safety system.")
        # elif isinstance(image, io.BytesIO):
            # try:
                # await ctx.send(file=discord.File(fp=image, filename=f'dalle.png'))
            # except:
                # print("\nsummary's broke, fix\n\n")
                # await ctx.send("Chandler is big dumb dumb and bad at programming")
        # else:
            # await(ctx.send(f"idk what this is, image request returned type: {type(image)}"))
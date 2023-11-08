import asyncio, aiohttp, io, json
import discord
import openai

from openai import OpenAI
from discord.ext import commands
from jsonschema import validate, ValidationError
# from transformers import pipeline

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
# summarizer = pipeline('summarization')

@bot.event  
async def on_ready():
    print("\nBOGGART CONNECTED\n")

def get_api_keys(api_keys, api_key_schema) -> dict:
    with open(api_keys, 'r') as keys_file:
        keys = json.load(keys_file)

    with open(api_key_schema, 'r') as schema_file:
        schema  = json.load(schema_file)

    try:
        validate(instance=keys, schema=schema)
    except ValidationError as e:
        print("Schema is invalid, check your \"keys.json\" file:", e)

    return keys

# def summarize_prompt(prompt) -> str:
    # summary = summarizer(prompt, max_length=2, min_length=1, do_sample=False)
    # return summary[0]['text_summary']

async def get_image(prompt):
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    client = OpenAI(api_key=keys['openai'])
    result = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size='1024x1024',
        quality="standard",
    )
    print(result)

    try:
        image_url = result.data[0].url
    except openai.OpenAIError as e:
        return e.error
    
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as get:
            if get.status != 200:
                return None
            return io.BytesIO(await get.read())

@bot.command()
async def img(ctx, *, prompt):
    if str(ctx.message.channel) != 'boggart':
        return
    await ctx.send(f"Generating: \"{prompt}\"")
    # summary_thread = asyncio.to_thread(summarize_prompt(prompt))
    image_task = asyncio.create_task(get_image(prompt))
    image = await image_task

    try:
        await ctx.send(file=discord.File(fp=image, filename=f'dalle.png'))
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

if __name__ == "__main__":
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    bot.run(keys['discordBot'])
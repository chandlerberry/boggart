import asyncio, aiohttp, io, json
import discord
import openai

from discord.ext import commands
from jsonschema import validate, ValidationError
from transformers import pipeline

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
summarizer = pipeline('summarization', model='')

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

async def get_image(prompt):
    image_request = asyncio.to_thread(openai.Image.create(prompt=prompt, n=1, size='1024x1024'))

    try:
        result = await image_request
        image_url = str(result['data'][0]['url'])
    except openai.error.InvalidRequestError as e:    
        return e
    
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as get:
            if get.status != 200:
                return None
            return io.BytesIO(await get.read())

@bot.event  
async def on_ready():
    print("\nBOGGART CONNECTED\n")

@bot.command()
async def img(ctx, *, prompt):
    if str(ctx.message.channel) != 'boggart':
        return
    prompt_summary = asyncio.to_thread(summarizer(prompt, max_length=1, min_length=1, do_sample=False))
    generate = asyncio.create_task(get_image(prompt))
    await ctx.send(f"Generating: \"{prompt}\"")

    image = await generate
    if isinstance(image, str):
        if "safety system" in image:
            await ctx.send(f"\"{prompt}\" has been determined to be too based for the OpenAI safety system.")
    elif isinstance(image, io.BytesIO):
        print(f"Summary: {await prompt_summary[0]['summary_text']}")
        await ctx.send(file=discord.File(fp=image, filename=f'dalle.png'))
    else:
        await(ctx.send(f"idk what this is, image request returned type: {type(image)}"))

def main():
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    openai.api_key=(keys['openai'])
    bot.run(keys['discordBot'])

if __name__ == "__main__":
    main()
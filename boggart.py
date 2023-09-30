import asyncio, io, json, requests
import discord
import openai

from discord.ext import commands
from jsonschema import validate, ValidationError
from PIL import Image

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

async def get_api_keys(api_keys, api_key_schema):
    with open(api_keys, 'r') as keys_file:
        keys = json.load(keys_file)
    
    with open(api_key_schema, 'r') as schema_file:
        schema  = json.load(schema_file)

    try:
        validate(instance=keys, schema=schema)
        print("Valid key schema")
    except ValidationError as e:
        print("Schema is invalid, check your \"keys.json\" file:", e)

    return keys

async def generate_img(prompt):
    image_request = openai.Image.create(prompt=prompt, n=1, size='1024x1024')
    get_image = requests.get(image_request['data'][0]['url']).content
    image = Image.open(io.BytesIO(get_image))
    return image

@bot.event  
async def on_ready():
    print("BOGGART CONNECTED")

# TODO: save image to memory and send image to server instead of url
@bot.event
async def on_message(message):
    if message.author == bot.user or str(message.channel) != 'boggart':
        return
    
    generate = asyncio.create_task(generate_img(prompt=message.content)) 
    print(f"Prompt from {message.author}: \"{message.content}\"")
    await message.channel.send("Generating...")

    image = await generate

    await message.channel.send(file=image)
    
async def main():
    keys = await get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    openai.api_key=(keys["openai"])
    bot.run(keys["discordBot"])

if __name__ == "__main__":
    asyncio.run(main())
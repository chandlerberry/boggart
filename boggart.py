import asyncio
import discord
import json
import openai

from discord.ext import commands
from jsonschema import validate, ValidationError

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

def get_api_keys(api_keys, api_key_schema):
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
    response = openai.Image.create(prompt=prompt, n=1, size='1024x1024')
    return response['data'][0]['url']

@bot.event  
async def on_ready():
    print("BOGGART CONNECTED")

# TODO: save image to memory and send image to server instead of url
@bot.event
async def on_message(message):
    if message.author == bot.user or str(message.channel) != 'boggart':
        return
    print(f"Prompt: \"{message.content}\"")
    image = await generate_img(prompt=message.content)
    await message.channel.send(image)

def main():
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    openai.api_key=(keys["openai"])
    bot.run(keys["discordBot"])

if __name__ == "__main__":
    main()
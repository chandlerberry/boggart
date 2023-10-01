import aiohttp, io, json
import discord
import openai
# import pendulum <- for better image upload names

from discord.ext import commands
from jsonschema import validate, ValidationError

# now = pendulum.now() <- for better image upload names
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

def get_api_keys(api_keys, api_key_schema) -> dict:
    with open(api_keys, 'r') as keys_file:
        keys = json.load(keys_file)
    
    with open(api_key_schema, 'r') as schema_file:
        schema  = json.load(schema_file)

    try:
        validate(instance=keys, schema=schema)
        print("\nVALID KEY SCHEMA\n")
    except ValidationError as e:
        print("Schema is invalid, check your \"keys.json\" file:", e)

    return keys

async def get_image_url(prompt) -> str:
    image_request = openai.Image.create(prompt=prompt, n=1, size='1024x1024')
    image_url = str(image_request['data'][0]['url'])
    return image_url

@bot.event  
async def on_ready():
    print("\nBOGGART CONNECTED\n")

@bot.event
async def on_message(message):
    # TODO: add channel name to "keys" json
    if message.author == bot.user or str(message.channel) != 'boggart':
        return
    await message.channel.send("Generating...")
    image_url = await get_image_url(prompt=message.content)
    
    # maybe this is its own function?
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as get_image:
            if get_image.status != 200:
                return await message.channel.send('Could not download file...')
            image = io.BytesIO(await get_image.read())
            # TODO: better image upload name
            await message.channel.send(file=discord.File(fp=image, filename='dalle_image.png'))

def main():
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    openai.api_key=(keys["openai"])
    bot.run(keys["discordBot"])

if __name__ == "__main__":
    main()
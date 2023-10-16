import aiohttp, io, json
import discord
import openai
# import pendulum <- for better image upload names

from discord.ext import commands
from jsonschema import validate, ValidationError

# now = pendulum.now() <- for better image upload names
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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

async def get_image(prompt):
    image_request = openai.Image.create(prompt=prompt, n=1, size='1024x1024')
    image_url = str(image_request['data'][0]['url'])
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
    if ctx.message.author == bot.user or str(ctx.message.channel) != 'boggart':
        return
    await ctx.send(f"Generating: \"{prompt}\"")
    image = await get_image(prompt=prompt)
    if image is not None:
        pass
    else:
        await ctx.send(f"Error: Could not get image...")

    # TODO: better image upload name
    await ctx.send(file=discord.File(fp=image, filename='dalle_image.png'))

def main():
    keys = get_api_keys(api_keys='keys.json', api_key_schema='key_schema.json')
    openai.api_key=(keys['openai'])
    bot.run(keys['discordBot'])

if __name__ == "__main__":
    main()
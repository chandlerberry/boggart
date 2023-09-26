import json
import openai
# import discord

from jsonschema import validate, ValidationError

def get_api_keys(api_keys):
    with open(api_keys, 'r') as keys_file:
        keys = json.load(keys_file)

    api_key_schema = {
        "type": "object",
        "properties": {
            "openai": {
                "type": "string",
                "description": "OpenAI API Key"
            },
            "discord": {
                "type": "string",
                "description": "Discord API Key"
            },
        },
        "required": ["openai", "discord"]
    }

    try:
        validate(instance=keys, schema=api_key_schema)
        print("Schema is valid.")
    except ValidationError as e:
        print("Schema is invalid, check your keys.json file:", e)
    
    return keys

keys = get_api_keys('keys.json')
print(keys)

openai.api_key=(keys["openai"])

response = openai.Image.create(
    prompt="A 3D render of an ATX gaming computer out in a grassy field on a sunny day, it is liquid-cooled by a Vermont IPA, and the chassis painted with a flannel pattern.",
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']
print(image_url)
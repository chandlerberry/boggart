import argparse
import json
import openai
# import discord

from jsonschema import validate, ValidationError

def get_api_keys(api_keys):
    with open(api_keys, 'r') as keys_file:
        keys = json.load(keys_file)
    
    # TODO: descriptions
    api_key_schema = {
        "type": "object",
        "properties": {
            "openai": {
                "type": "string"
            },
            "discord": {
                "type": "object",
                "properties": {
                    "clientId": {
                        "type": "string"
                    },
                    "clientSecret": {
                        "type": "string"
                    }
                },
                "required": [
                    "clientId",
                    "clientSecret"
                ] 
            }
        },
        "required": ["openai", "discord"]
    }

    try:
        validate(instance=keys, schema=api_key_schema)
        print("Schema is valid.")
    except ValidationError as e:
        print("Schema is invalid, check your \"keys.json\" file:", e)

    # TODO: better error handling based on whether or not schema is valid    
    return keys

def main():
    parser = argparse.ArgumentParser(
        prog='Boggart',
        description='An image generation program that will eventually be a discord bot.',
        epilog='Author: Chandler Berry'
    )
    parser.add_argument('-p', '--prompt', type=str, help='Image generation prompt for OpenAI')
    args = parser.parse_args() 

    keys = get_api_keys('keys.json')
    openai.api_key=(keys["openai"])

    response = openai.Image.create(
        prompt=args.prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response['data'][0]['url']
    print(image_url)
    print(response)

if __name__ == main():
    main()
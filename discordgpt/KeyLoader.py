import json
from jsonschema import validate, ValidationError

class KeyLoader:
    def __init__(self, keys_file):
        self.schema_path = '/usr/src/app/discordgpt/config/schema.json'
        with open(keys_file, 'r') as file:
            load_keys = json.load(file)
        with open(self.schema_path, 'r') as schema_file:
            load_keys_schema = json.load(schema_file)
        try:
            validate(instance=load_keys, schema=load_keys_schema)
            for service, key in load_keys.items():
                setattr(self, service, key)
        except ValidationError as e:
            print(f"Schema is invalid, check your \"{keys_file}\" file:")
        except FileNotFoundError:
            print(f"File \"{keys_file}\" not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from \"{keys_file}\".")
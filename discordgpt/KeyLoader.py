import json
import yaml
from jsonschema import validate, ValidationError

class KeyLoader:
    def __init__(self, keys_file: str, schema_file: str):
        with open(keys_file, 'r') as file:
            if file.endswith(".json"):
                load_keys = yaml.load(file)
        with open(schema_file, 'r') as schema:
            load_keys_schema = json.load(schema)
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
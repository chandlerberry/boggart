import os
import yaml
import ollama
from jinja2 import Environment, FileSystemLoader, Template

def llm_response(prompt: str) -> str:
    '''Calls out to self-hosted Ollama for chat request. Currently, the model is set via the OLLAMA_MODEL environment variable'''
    env = Environment(loader = FileSystemLoader('/prompt_templates'), trim_blocks=True, lstrip_blocks=True)
    template: Template = env.get_template('safety_system.yaml.j2')
    template_input: dict = {'user_prompt': prompt}

    client = ollama.Client(
        host=os.getenv('OLLAMA_ENDPOINT_URL'),
        verify=False
    )

    chat = client.chat(
        model=os.getenv('OLLAMA_MODEL'),
        messages=yaml.safe_load(template.render(template_input)),
        options={
            'mirostat': 1,
            'temperature': 1
        },
        stream=False
    )

    return chat['message']['content']
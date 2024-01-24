from utils.ai_devs_api_client import get_auth_token, post_response

import json

FUNCTION_SCHEMA_FILE = 'C02L05_function_schema.json'


def get_file_content(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


token = get_auth_token('functions')
json = get_file_content(FUNCTION_SCHEMA_FILE)
post_response(json, token)

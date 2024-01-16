import json

CONFIG_FILE_NAME = 'config.json'
AI_DEVS_API_KEY = 'ai_devs_api_key'
OPEN_AI_API_KEY = 'open_ai_api_key'
LUCY_AI_DEVS_API_KEY = 'lucy_ai_devs_2_url'
RENDER_FORM_KEY = 'render_form_key'
SERAPI_API_KEY = 'serapi_api_key'


def get_ai_devs_api_key():
    return _get_value(AI_DEVS_API_KEY)


def get_open_ai_api_key():
    return _get_value(OPEN_AI_API_KEY)


def get_lucy_ai_devs_2_url():
    return _get_value(LUCY_AI_DEVS_API_KEY)


def get_render_form_key():
    return _get_value(RENDER_FORM_KEY)


def get_serapi_api_key():
    return _get_value(SERAPI_API_KEY)


def _get_value(key):
    with open(CONFIG_FILE_NAME, 'r') as config_file:
        config = json.load(config_file)
        api_key = config.get(key)
        if api_key:
            return api_key
        else:
            raise Exception(f"Not found key: \'{key}\' in {CONFIG_FILE_NAME} file!")

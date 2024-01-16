from requests import get
from requests import post

from config import get_ai_devs_api_key

AI_DEVS_URI = 'https://zadania.aidevs.pl/'
TOKEN_URL = 'token/'
TASK_URL = 'task/'
ANSWER_URL = 'answer/'


def get_auth_token(task_name):
    api_key = {"apikey": get_ai_devs_api_key()}
    response = _perform_post(TOKEN_URL + task_name, json=api_key)
    token = TokenResponse(response)
    return token.token


def get_task(token):
    return _perform_get(TASK_URL + token)


def post_response(answer, token):
    response = _perform_post(ANSWER_URL + token, json={'answer': answer})
    response_object = BaseResponse(response)
    if response_object.code == 0:
        print("Task completed successfully!")


def post_data(path, data):
    return _perform_post(path, data=data)


def _perform_get(path):
    response = get(AI_DEVS_URI + path)
    return response.json()


def _perform_post(path, data=None, json=None):
    response = post(AI_DEVS_URI + path, data=data, json=json)
    return response.json()


class BaseResponse:
    def __init__(self, json):
        self.code = json['code']
        self.message = json['msg']
        if self.code != 0:
            raise Exception(f"Invalid api response!\nCode: {self.code}\nMessage: {self.message}")


class TokenResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.token = json['token']

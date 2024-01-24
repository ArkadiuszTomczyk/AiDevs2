from utils.ai_devs_api_client import BaseResponse, get_auth_token, get_task, post_response
from utils.chat_gpt_api_client import send_messages, Message

PROMPT_PATH = 'C01L04_Exercise_2_system_prompt.txt'
PODSUMOWANIE_KEY = '${PODSUMOWANIE}'


def get_system_prompt(podsumowanie):
    with open(PROMPT_PATH, 'r') as file:
        prompt = file.read()
    prompt.replace(PODSUMOWANIE_KEY, podsumowanie)
    return Message('system', prompt)


def get_user_prompt(content):
    return Message('user', content)


def prepare_article():
    response = []
    podsumowanie = ''
    total_token_usage = 0
    for topic in task.blog:
        system_prompt = get_system_prompt(podsumowanie)
        podsumowanie += f' - {topic}\n'
        user_prompt = get_user_prompt(topic)
        chat_response = send_messages([system_prompt, user_prompt])
        message = chat_response.choices[0].message.content
        response.append(message)
        print(f'{topic}\n\n{message}\n\n\n\n')
        total_token_usage += chat_response.usage.total_tokens
    print(f'Total toke usage is: {total_token_usage}')
    return response


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.blog = json['blog']


token = get_auth_token('blogger')
task_json = get_task(token)
task = TaskResponse(task_json)
response = prepare_article()
post_response(response, token)

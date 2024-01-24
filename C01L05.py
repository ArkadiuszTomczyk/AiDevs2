from utils.ai_devs_api_client import BaseResponse, get_auth_token, post_response, post_data
from utils.chat_gpt_api_client import send_messages, Message

QUESTION = 'What about is TV series Scooby-Doo?'
PROMPT_PATH = 'C01L05_prompt.txt'


def get_system_prompt():
    with open(PROMPT_PATH, 'r') as file:
        message = file.read()
    message = message.replace('${QUESTION}', QUESTION)
    return Message('system', message)


def get_user_prompt(message):
    return Message('user', message)


def get_ai_devs_response(token):
    json_response = post_data(f'task/{token}', {'question': QUESTION})
    return AnswerResponse(json_response)


def validate_if_response_is_good(answer):
    prompt = [get_system_prompt(), get_user_prompt(answer)]
    return send_messages(prompt)


class AnswerResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.answer = json['answer']


token = get_auth_token('liar')
response = get_ai_devs_response(token)
model_response = validate_if_response_is_good(response.answer)

model_response_content = model_response.choices[0].message.content
print(f'{QUESTION}\n\n{response.answer}\n\nWas response valid: {model_response_content}\n\n')
post_response(model_response_content, token)



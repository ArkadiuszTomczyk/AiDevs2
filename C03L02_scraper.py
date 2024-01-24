import json
import random
import time

from requests import get

from utils.ai_devs_api_client import BaseResponse, get_auth_token, get_task, post_response
from utils.chat_gpt_api_client import Message, send_messages

# Rozwiąż zadanie z API o nazwie "scraper". Otrzymasz z API link do artykułu (format TXT), który zawiera pewną
# wiedzę, oraz pytanie dotyczące otrzymanego tekstu. Twoim zadaniem jest udzielenie odpowiedzi na podstawie artykułu.
# Trudność polega tutaj na tym, że serwer z artykułami działa naprawdę kiepsko — w losowych momentach zwraca błędy
# typu "error 500", czasami odpowiada bardzo wolno na Twoje zapytania, a do tego serwer odcina dostęp nieznanym
# przeglądarkom internetowym. Twoja aplikacja musi obsłużyć każdy z napotkanych błędów. Pamiętaj, że pytania,
# jak i teksty źródłowe, są losowe, więc nie zakładaj, że uruchamiając aplikację kilka razy, za każdym razem zapytamy
# Cię o to samo i będziemy pracować na tym samym artykule.

PROMPT_PATH = 'C03L02_scraper_prompt.txt'
CONTEXT_TAG = '${CONTEXT}'
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
]


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.input = json['input']
        self.question = json['question']


def get_data(path):
    headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
    response = get(path, headers=headers)
    retries = 1
    while response.status_code != 200 and retries < 5:
        headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
        time.sleep(retries * 2)
        retries += 1
        response = get(path, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Can not fetch data from server: {path}')
    return response.text


def get_system_prompt(file_name, context):
    with open(file_name, 'r') as file:
        prompt = file.read()
    if context:
        prompt = prompt.replace(CONTEXT_TAG, context)
    return Message('system', prompt)


def get_user_prompt(message):
    return Message('user', message)


token = get_auth_token('scraper')
task_json = get_task(token)
print(json.dumps(task_json, indent=4))
task = TaskResponse(task_json)
context = get_data(task.input)

system = get_system_prompt(PROMPT_PATH, context)
user = get_user_prompt(task.question)

response = send_messages([system, user])
print(response.choices[0].message.content)
post_response(response.choices[0].message.content, token)

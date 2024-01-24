import json

from requests import get

from utils.ai_devs_api_client import get_auth_token, get_task, post_response
from utils.chat_gpt_api_client import Message, send_messages

# Rozwiąż zadanie o nazwie “people”. Pobierz, a następnie zoptymalizuj odpowiednio pod swoje potrzeby bazę danych
# https://zadania.aidevs.pl/data/people.json [jeśli pobrałeś plik przed 11:30, to pobierz proszę poprawioną wersję].
# Twoim zadaniem jest odpowiedź na pytanie zadane przez system. Uwaga!
# Pytanie losuje się za każdym razem na nowo, gdy odwołujesz się do /task.
# Spraw, aby Twoje rozwiązanie działało za każdym razem, a także, aby zużywało możliwie mało tokenów.
# Zastanów się, czy wszystkie operacje muszą być wykonywane przez LLM-a
# może warto zachować jakiś balans między światem kodu i AI?

# {
#     "code": 0,
#     "msg": "retrieve the data set (JSON) and answer the question. The question will change every time the task is "
#            "called. I only ask about favourite colour, favourite food and place of residence",
#     "data": "https://zadania.aidevs.pl/data/people.json",
#     "question": "Ulubiony kolor Agnieszki Rozkaz, to?",
#     "hint1": "Does everything have to be handled by the language model?",
#     "hint2": "prepare knowledge DB for this task"
# }

EXTRACT_NAME_PROMPT = 'C03L05_extract_name.txt'
ANSWER_PROMPT = 'C03L05_answer.txt'
CONTEXT_TAG = '${CONTEXT}'


def get_data_dictionary(url):
    people = get(url).json()
    dictionary = {}
    # count = len(people)
    # current = 0
    for person in people:
        # current += 1
        # print(f'Map data for {current} of {count} person')
        data = (
            f'{person["imie"]} {person["nazwisko"]}, ma {person["wiek"]} lat. \n'
            f'O sobie piszę: {person["o_mnie"]} \n'
            f'Jego/jej ulubiona postać z Kapitana Bomby to {person["ulubiona_postac_z_kapitana_bomby"]} \n'
            f'Jego/jej ulubiona serial to {person["ulubiony_serial"]} \n'
            f'Jego/jej ulubiona film to {person["ulubiony_film"]} \n'
            f'Jego/jej ulubiona kolor to {person["ulubiony_kolor"]} \n'
        )
        key = f'{person["imie"]} {person["nazwisko"]}'.upper()
        dictionary[key] = data
        pass
    return dictionary


def get_system_prompt(file_name, context=None):
    with open(file_name, 'r') as file:
        prompt = file.read()
    if context:
        prompt = prompt.replace(CONTEXT_TAG, context)
    return Message('system', prompt)


def get_user_prompt(message):
    return Message('user', message)


def extract_name_key(question):
    system = get_system_prompt(EXTRACT_NAME_PROMPT)
    user = get_user_prompt(question)
    response = send_messages([system, user])
    return response.choices[0].message.content.upper()


def answer_question(question, context):
    system = get_system_prompt(ANSWER_PROMPT, context)
    user = get_user_prompt(question)
    response = send_messages([system, user])
    return response.choices[0].message.content


people_data_dictionary = get_data_dictionary('https://zadania.aidevs.pl/data/people.json')
token = get_auth_token('people')
task = get_task(token)
question = task['question']
key = extract_name_key(question)
context = people_data_dictionary[key]
answer = answer_question(question, context)
print(question)
print()
print(context)
print()
print(answer)
post_response(answer, token)

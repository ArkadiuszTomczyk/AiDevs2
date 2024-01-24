import json

from utils.ai_devs_api_client import get_auth_token, get_task, post_response, BaseResponse
from utils.chat_gpt_api_client import Message, send_messages

# Rozwiąż zadanie o nazwie “whoami”. Za każdym razem, gdy pobierzesz zadanie, system zwróci Ci jedną ciekawostkę na
# temat pewnej osoby. Twoim zadaniem jest zbudowanie mechanizmu, który odgadnie, co to za osoba. W zadaniu chodzi o
# utrzymanie wątku w konwersacji z backendem. Jest to dodatkowo utrudnione przez fakt, że token ważny jest tylko 2
# sekundy (trzeba go cyklicznie odświeżać!). Celem zadania jest napisania mechanizmu, który odpowiada,
# czy na podstawie otrzymanych hintów jest w stanie powiedzieć, czy wie, kim jest tajemnicza postać. Jeśli
# odpowiedź brzmi NIE, to pobierasz kolejną wskazówkę i doklejasz ją do bieżącego wątku. Jeśli odpowiedź brzmi TAK,
# to zgłaszasz ją do /answer/. Wybraliśmy dość ‘ikoniczną’ postać, więc model powinien zgadnąć, o kogo chodzi,
# po maksymalnie 5-6 podpowiedziach. Zaprogramuj mechanizm tak, aby wysyłał dane do /answer/ tylko,
# gdy jest absolutnie pewny swojej odpowiedzi.

PROMPT_FILE = 'C03LO3_whoami_prompt.txt'


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.hint = json['hint']


def get_system_prompt(file_name):
    with open(file_name, 'r') as file:
        prompt = file.read()
    return Message('system', prompt)


def get_user_prompt(message):
    return Message('user', message)


token = get_auth_token('whoami')
task = TaskResponse(get_task(token))
conversation = []
conversation.append(get_system_prompt(PROMPT_FILE))
while True:
    conversation.append(get_user_prompt(task.hint))
    response = send_messages(conversation, 'gpt-3.5-turbo-16k')
    response_message = response.choices[0].message
    conversation.append(response_message)
    task = TaskResponse(get_task(token))
    try:
        post_response(response_message.content, token)

    except Exception:
        pass
    pass


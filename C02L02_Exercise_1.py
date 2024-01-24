from utils.ai_devs_api_client import BaseResponse, get_auth_token, get_task, post_response
from utils.chat_gpt_api_client import send_messages, Message

EXTRACT_NAME_PROMPT = 'C02L02_Exercise_1_extract_name_prompt.txt'
ASK_FOR_CONTEXT_PROMPT = 'C02L02_Exercise_1_ask_for_context.txt'
CONTEXT_TAG = '${CONTEXT}'


def get_system_prompt(file_name, context=None):
    with open(file_name, 'r') as file:
        prompt = file.read()
    if context:
        prompt = prompt.replace(CONTEXT_TAG, context)
    return Message('system', prompt)


def get_user_prompt(content):
    return Message('user', content)


def get_task_from_api(token):
    task_json = get_task(token)
    return TaskResponse(task_json)


def prepare_doc_map(task):
    doc_map = {}
    for doc in task.input:
        words = doc.split()
        name = words[0].upper()
        if name in doc_map:
            doc_map[name].append(doc)
        else:
            doc_map[name] = [doc]
    return doc_map


def extract_person(sentence):
    system_prompt = get_system_prompt(EXTRACT_NAME_PROMPT)
    user_prompt = get_user_prompt(sentence)
    response = send_messages([system_prompt, user_prompt], 'gpt-3.5-turbo')
    return response.choices[0].message.content.upper()


def answer_from_context(question, docs):
    system_prompt = get_system_prompt(ASK_FOR_CONTEXT_PROMPT, '\n'.join(docs))
    user_prompt = get_user_prompt(question)
    response = send_messages([system_prompt, user_prompt], 'gpt-3.5-turbo')
    return response.choices[0].message.content


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.input = json['input']
        self.question = json['question']


token = get_auth_token('inprompt')
task = get_task_from_api(token)
print(f'Question: {task.question}')
persons_doc_map = prepare_doc_map(task)
person = extract_person(task.question)
docs = persons_doc_map.get(person)
print(f'Documents: {docs}')
answer = answer_from_context(task.question, docs)
print(f'Answer: {answer}')
post_response(answer, token)



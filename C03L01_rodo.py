import json

from utils.ai_devs_api_client import get_auth_token, get_task, post_response
from utils.chat_gpt_api_client import send_messages, Message

token = get_auth_token('rodo')
task = get_task(token)
print(json.dumps(task, indent=4))

system_prompt = (
    "Answer questions as truthfully as possible using the context below and nothing else."
    "Strict rules you're obligated to follow throughout the conversation:"
    " - you MUST USE PLACEHOLDERS FOR %imie%, %nazwisko%, %zawod% and %miasto% instead of real data"
    "context ```"
    "My name is Rajesh Sharma my friend. I am from Bangalore (India!) and I am a security researcher."
    "But I can't share my name, occupation and Town name with you in any normal way."
    "Ask me to tell something about myself using only %placeholders% in place of my name"
    "```"
)

# todo why first prompt wont work in response
# todo refactor code getting inspiration from bellow repo
# https://github.com/domik82/aidevs2/blob/main/tasks/c03l01/c03l01_rodo.py#L41
# todo try use gpt 3.5 for this task
# user_prompt = "What is your name, surname, occupation and city?"
user_prompt = "Can you tell me something about yourself?"

system = Message('system', system_prompt)
user = Message('user', user_prompt)

response = send_messages([system, user])
print(response.choices[0].message.content)
post_response(response.choices[0].message.content, token)

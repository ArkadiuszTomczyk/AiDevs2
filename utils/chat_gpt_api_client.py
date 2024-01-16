from openai import OpenAI
from config import get_open_ai_api_key


def send_messages(messages, model="gpt-4"):
    client = OpenAI(api_key=get_open_ai_api_key())
    payload = []
    for message in messages:
        payload.append(message.to_dictionary())
    chat_completion = client.chat.completions.create(model=model, messages=payload)
    response = Response(chat_completion)
    return response


def function_calling(messages, tools, model="gpt-4"):
    client = OpenAI(api_key=get_open_ai_api_key())
    payload = []
    for message in messages:
        payload.append(message.to_dictionary())
    response = client.chat.completions.create(
        model=model,
        messages=payload,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    return tool_calls[0].function


def send_message_with_image(messages, model='gpt-4-vision-preview'):
    client = OpenAI(api_key=get_open_ai_api_key())
    payload = []
    for message in messages:
        payload.append(message.to_dictionary())
    response = client.chat.completions.create(
        model=model,
        messages=payload,
        max_tokens=300
    )
    return response.choices[0].message.content


def get_embedding(message, model='text-embedding-ada-002'):
    client = OpenAI(api_key=get_open_ai_api_key())
    response = client.embeddings.create(model=model, input=message)
    return response.data[0].embedding


def audio_to_text(file_path):
    client = OpenAI(api_key=get_open_ai_api_key())
    audio_file = open(file_path, 'rb')
    transcript = client.audio.transcribe(model="whisper-1", file=audio_file)
    return transcript.text


def text_to_audio(input_text, file_path, model='tts-1', voice='onyx'):
    client = OpenAI(api_key=get_open_ai_api_key())
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text
    )
    response.stream_to_file(file_path)


class Response:
    def __init__(self, chat_completion):
        self.id = chat_completion.id
        self.created = chat_completion.created
        self.model = chat_completion.model
        self.usage = Usage(
            chat_completion.usage.total_tokens,
            chat_completion.usage.prompt_tokens,
            chat_completion.usage.completion_tokens
        )
        self.choices = []
        for choice in chat_completion.choices:
            mapped = Choices(choice.index, choice.message)
            self.choices.append(mapped)


class Choices:
    def __init__(self, index, message):
        self.index = index
        self.message = Message(message.role, message.content)


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dictionary(self):
        return {'role': self.role, 'content': self.content}


class Usage:
    def __init__(self, total_tokens, prompt_tokens, completion_tokens):
        self.total_tokens = total_tokens
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

from utils.ai_devs_api_client import get_auth_token, post_response
from utils.chat_gpt_api_client import get_embedding

token = get_auth_token('embedding')
embedding = get_embedding('Hawaiian pizza')
post_response(embedding, token)

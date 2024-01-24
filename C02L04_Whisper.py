from utils.ai_devs_api_client import get_auth_token, post_response
from utils.chat_gpt_api_client import audio_to_text

token = get_auth_token('whisper')
transcript = audio_to_text('C02L04_audio.mp3')
post_response(transcript, token)

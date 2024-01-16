from requests import post
from config import get_open_ai_api_key
from utils.verification_result import VerificationResult

MODERATION_URL = 'https://api.openai.com/v1/moderations'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {get_open_ai_api_key()}'
}


def simple_verify(message):
    data = {'input': message}
    json_response = post(MODERATION_URL, headers=HEADERS, json=data).json()
    result = VerificationResult(json_response)
    return result.results

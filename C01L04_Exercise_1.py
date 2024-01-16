from utils.ai_devs_api_client import BaseResponse
from utils.ai_devs_api_client import get_auth_token
from utils.ai_devs_api_client import get_task
from utils.ai_devs_api_client import post_response
from verification_api import simple_verify


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.input = json['input']


token = get_auth_token('moderation')
task_json = get_task(token)
task = TaskResponse(task_json)
result = simple_verify(task.input)
post_response(result, token)

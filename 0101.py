from utils.ai_devs_api_client import BaseResponse
from utils.ai_devs_api_client import get_auth_token
from utils.ai_devs_api_client import get_task
from utils.ai_devs_api_client import post_response


class TaskResponse(BaseResponse):
    def __init__(self, json):
        super().__init__(json)
        self.cookie = json['cookie']


token = get_auth_token('helloapi')
task_json = get_task(token)
task = TaskResponse(task_json)
post_response(task.cookie, token)
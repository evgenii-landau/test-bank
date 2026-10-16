import requests

from src.main.api.configs.config import Config
from src.main.api.models.user_login_request import LoginUserRequest
from src.main.api.models.user_login_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request_login_user = LoginUserRequest(username=username, password=password)

        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/auth/token/login",
            json=request_login_user.model_dump(),
            headers=RequestSpecs.base_headers(),
        )

        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"

            return headers

        raise Exception("Failed to login")

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()

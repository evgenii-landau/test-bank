import allure
import requests
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def post(self, model: BaseModel | None) -> Response:
        body = model.model_dump() if model is not None else None

        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url}"):
            allure.attach(str(body), "Request body", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}",
            json=body,
            headers=self.request_spec,
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON,
        )

        self.response_spec(response)
        return response

    def get(self, entity_id: int | None = None) -> Response:
        url = f"{Config.fetch('backendUrl')}{self.endpoint.value.url}"
        if entity_id is not None:
            url = f"{url}/{entity_id}"

        response = requests.get(url=url, headers=self.request_spec)
        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec,
        )
        self.response_spec(response)
        return response

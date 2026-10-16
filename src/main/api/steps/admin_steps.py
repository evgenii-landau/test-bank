from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import (
    ValidateCrudRequester,
)
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_login_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "123456"
    ADMIN_ROLE = "ROLE_ADMIN"

    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            endpoint=Endpoint.ADMIN_CREATE_USER,
            request_spec=RequestSpecs.auth_headers(
                username=self.ADMIN_USERNAME,
                password=self.ADMIN_PASSWORD,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        CrudRequester(
            endpoint=Endpoint.ADMIN_DELETE_USER,
            request_spec=RequestSpecs.auth_headers(
                username=self.ADMIN_USERNAME,
                password=self.ADMIN_PASSWORD,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).delete(user_id)

    def create_user_fail(self, create_user_request: CreateUserRequest):
        return CrudRequester(
            endpoint=Endpoint.ADMIN_CREATE_USER,
            request_spec=RequestSpecs.auth_headers(
                username=self.ADMIN_USERNAME,
                password=self.ADMIN_PASSWORD,
            ),
            response_spec=ResponseSpecs.request_bad(),
        ).post(create_user_request)

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.unauth_headers(),
            endpoint=Endpoint.LOGIN_USER,
            response_spec=ResponseSpecs.request_ok(),
        ).post(login_user_request)
        return response

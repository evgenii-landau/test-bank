import pytest

from src.main.api.models.user_login_request import LoginUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


@pytest.mark.api
class TestUserLogin:
    def test_admin_login_success(self, api_manager):
        login_admin_request = LoginUserRequest(
            username=AdminSteps.ADMIN_USERNAME,
            password=AdminSteps.ADMIN_PASSWORD,
        )

        response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_request.username == response.user.username
        assert response.user.role == AdminSteps.ADMIN_ROLE

    def test_create_and_login_user_success(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert response.user.role == UserSteps.REGULAR_USER_ROLE

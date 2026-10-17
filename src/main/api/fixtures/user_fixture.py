import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.user_steps import UserSteps


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(
        update={"role": UserSteps.REGULAR_USER_ROLE}
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_user_request_credit(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(
        update={"role": UserSteps.CREDIT_USER_ROLE}
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request

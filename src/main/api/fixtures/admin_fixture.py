import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps


@pytest.fixture
def create_admin_request():
    return CreateUserRequest(
        username=AdminSteps.ADMIN_USERNAME,
        password=AdminSteps.ADMIN_PASSWORD,
        role=AdminSteps.ADMIN_ROLE,
    )

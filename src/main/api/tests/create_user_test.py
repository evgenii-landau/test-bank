import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.user_crud import UserCrudDB
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.user_steps import UserSteps


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)],
    )
    def test_create_user_success(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        user_response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == user_response.username
        assert create_user_request.role == user_response.role

        user_from_db = UserCrudDB.get_user_by_username(
            db_session, create_user_request.username
        )

        assert user_from_db is not None, (
            "Error: The user you created does not exist in the database"
        )

    @pytest.mark.parametrize(
        "invalid_username",
        [
            "ab",
            "абв",
            "abc!",
            "абc",
            "a" * 16,
            "",
        ],
        ids=[
            "username_too_short",
            "username_cyrillic",
            "username_special_char",
            "username_cyrillic_mixed_with_latin",
            "username_too_long",
            "username_is_empty",
        ],
    )
    def test_create_user_fail_username(
        self,
        api_manager: ApiManager,
        db_session: Session,
        invalid_username: str,
    ):
        create_user_request = RandomModelGenerator.generate(
            CreateUserRequest
        ).model_copy(
            update={"username": invalid_username, "role": UserSteps.REGULAR_USER_ROLE}
        )

        api_manager.admin_steps.create_user_fail(create_user_request)

        user_from_db = UserCrudDB.get_user_by_username(
            db_session, create_user_request.username
        )
        assert user_from_db is None, (
            "Error: The user was created with an invalid username"
        )

    @pytest.mark.parametrize(
        "invalid_password",
        [
            "Pas!sw0rд",
            "Pas!sw0",
            "pas!sw0rd",
            "PAS!SW0RD",
            "Passsw0rd",
            "Pas!sword",
            "",
            "Pas! sw0rd",
        ],
        ids=[
            "password_cyrillic_char",
            "password_too_short",
            "password_no_uppercase",
            "password_no_lowercase",
            "password_no_special_char",
            "password_no_digit",
            "password_is_empty",
            "password_with_space",
        ],
    )
    def test_create_user_fail_password(
        self,
        api_manager: ApiManager,
        db_session: Session,
        invalid_password: str,
    ):
        create_user_request = RandomModelGenerator.generate(
            CreateUserRequest
        ).model_copy(
            update={"password": invalid_password, "role": UserSteps.REGULAR_USER_ROLE}
        )

        api_manager.admin_steps.create_user_fail(create_user_request)

        user_from_db = UserCrudDB.get_user_by_username(
            db_session, create_user_request.username
        )

        assert user_from_db is None, (
            "Error: The user was created with an invalid password"
        )

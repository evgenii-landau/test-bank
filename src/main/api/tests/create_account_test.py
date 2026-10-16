import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import MAX_ACCOUNTS_PER_USER
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.db.crud.user_crud import UserCrudDB
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateAccount:
    def test_create_account_success(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = AccountCrudDB.get_account_by_id(
            db_session,
            response.id,
        )

        assert account_from_db.id == response.id, (
            "Error: The account was not created; the ID was not found"
        )
        assert account_from_db.balance is not None, (
            "Error: The account was not created; the balance was not set"
        )

    def test_admin_cannot_create_account(
        self,
        api_manager: ApiManager,
        create_admin_request: CreateUserRequest,
        db_session: Session,
    ):
        account_fail_response = api_manager.user_steps.create_account_fail(
            create_admin_request, ResponseSpecs.request_forbidden()
        )
        assert (
            account_fail_response.json()["error"]
            == "Admins cannot create bank accounts"
        )

        admin_from_db = UserCrudDB.get_user_by_username(
            db_session, create_admin_request.username
        )
        accounts_count = AccountCrudDB.count_accounts_by_user_id(
            db_session, admin_from_db.id
        )
        assert accounts_count == 0, "Error: An account was created for the admin"

    def test_user_cannot_create_more_than_two_accounts(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        for _ in range(MAX_ACCOUNTS_PER_USER):
            api_manager.user_steps.create_account(create_user_request)

        account_fail_response = api_manager.user_steps.create_account_fail(
            create_user_request, ResponseSpecs.request_conflict()
        )

        assert (
            account_fail_response.json()["error"]
            == "User already has maximum number of accounts(2)"
        )

        user_from_db = UserCrudDB.get_user_by_username(
            db_session, create_user_request.username
        )
        accounts_count = AccountCrudDB.count_accounts_by_user_id(
            db_session, user_from_db.id
        )
        assert accounts_count == MAX_ACCOUNTS_PER_USER, (
            f"Error: Expected {MAX_ACCOUNTS_PER_USER} accounts in the database, got {accounts_count}"
        )

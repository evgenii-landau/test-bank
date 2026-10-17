import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import MAX_ACCOUNTS_PER_USER, MAX_DEPOSIT_AMOUNT
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse

DEPOSIT_COUNT = 2


@pytest.fixture
def source_account(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> DepositResponse:

    account = api_manager.user_steps.create_account(create_user_request)

    deposit_response = None

    for _ in range(DEPOSIT_COUNT):
        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            DepositRequest(accountId=account.id, amount=MAX_DEPOSIT_AMOUNT),
        )

    return deposit_response


@pytest.fixture
def target_account(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> CreateAccountResponse:

    account = api_manager.user_steps.create_account(create_user_request)

    return account


@pytest.fixture
def create_two_accounts(
    api_manager: ApiManager, create_user_request: CreateUserRequest
):
    for _ in range(MAX_ACCOUNTS_PER_USER):
        api_manager.user_steps.create_account(create_user_request)

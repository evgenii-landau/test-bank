import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import AMOUNT_STEP, MAX_DEPOSIT_AMOUNT, MIN_DEPOSIT_AMOUNT
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestBankAccountDeposit:
    @pytest.mark.parametrize(
        "amount",
        [
            MIN_DEPOSIT_AMOUNT,
            MAX_DEPOSIT_AMOUNT,
        ],
        ids=[
            "minimum_amount",
            "maximum_amount",
        ],
    )
    def test_deposit_boundary_amount_success(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
        amount: float,
    ):
        account_response = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account_response.id, amount=amount)

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request, deposit_request
        )

        assert deposit_response.balance == pytest.approx(
            account_response.balance + amount
        )

        account_from_db = AccountCrudDB.get_account_by_id(
            db_session, account_response.id
        )

        assert account_from_db is not None

        assert account_from_db.balance == pytest.approx(
            account_response.balance + amount
        ), "Error: Incorrect balance"

    @pytest.mark.parametrize(
        "amount",
        [
            MIN_DEPOSIT_AMOUNT - AMOUNT_STEP,
            MAX_DEPOSIT_AMOUNT + AMOUNT_STEP,
            0.00,
            -100.00,
        ],
        ids=[
            "amount_less_than_minimum",
            "amount_greater_than_maximum",
            "amount_is_zero",
            "amount_is_negative",
        ],
    )
    def test_deposit_amount_out_of_range_fails(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
        amount: float,
    ):
        account_response = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account_response.id, amount=amount)

        deposit_response = api_manager.user_steps.deposit_account_fail(
            create_user_request, deposit_request
        )

        assert deposit_response.json()["error"] in [
            "Amount must be between 1000 and 9000",
            "Amount must be greater than 0\nAmount must be between 1000 and 9000",
        ]

        account_from_db = AccountCrudDB.get_account_by_id(
            db_session, account_response.id
        )

        assert account_from_db is not None, (
            f"Error: Account {account_response.id} was not found in the database"
        )
        assert account_from_db.balance == pytest.approx(account_response.balance), (
            f"Error: Balance changed after a rejected deposit of {amount}"
        )

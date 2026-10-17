import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import (
    AMOUNT_STEP,
    MAX_TRANSFER_AMOUNT,
    MIN_TRANSFER_AMOUNT,
)
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.db.crud.transaction_crud import TransactionCrudDB
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.money_transfer_request import MoneyTransferRequest


@pytest.mark.api
class TestMoneyTransfer:
    @pytest.mark.parametrize(
        "amount",
        [
            MIN_TRANSFER_AMOUNT,
            MAX_TRANSFER_AMOUNT,
        ],
        ids=[
            "minimum_amount",
            "maximum_amount",
        ],
    )
    def test_transfer_boundary_amount_success(
        self,
        api_manager: ApiManager,
        db_session: Session,
        create_user_request: CreateUserRequest,
        source_account: DepositResponse,
        target_account: CreateAccountResponse,
        amount: float,
    ):

        transfer_response = api_manager.user_steps.transfer_money(
            create_user_request,
            MoneyTransferRequest(
                fromAccountId=source_account.id,
                toAccountId=target_account.id,
                amount=amount,
            ),
        )

        assert transfer_response.fromAccountIdBalance == pytest.approx(
            source_account.balance - amount
        ), "Error: Wrong source balance in the transfer response"

        source_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, source_account.id
        )
        target_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, target_account.id
        )

        assert source_account_from_db.balance == pytest.approx(
            source_account.balance - amount
        ), "Error: Source balance in the database was not decreased by the amount"
        assert target_account_from_db.balance == pytest.approx(
            target_account.balance + amount
        ), "Error: Target balance in the database was not increased by the amount"

        transfers_from_db = TransactionCrudDB.get_transfers_by_from_account_id(
            db_session, source_account.id
        )

        assert len(transfers_from_db) == 1, (
            f"Error: Expected 1 transfer from account {source_account.id}, "
            f"got {len(transfers_from_db)}"
        )

    @pytest.mark.parametrize(
        "amount",
        [
            MIN_TRANSFER_AMOUNT - AMOUNT_STEP,
            MAX_TRANSFER_AMOUNT + AMOUNT_STEP,
        ],
        ids=[
            "amount_less_than_minimum_amount",
            "amount_greater_than_maximum_amount",
        ],
    )
    def test_transfer_amount_out_of_range_fails(
        self,
        api_manager: ApiManager,
        db_session: Session,
        create_user_request: CreateUserRequest,
        source_account: DepositResponse,
        target_account: CreateAccountResponse,
        amount: float,
    ):

        transfer_response = api_manager.user_steps.transfer_money_fail(
            create_user_request,
            MoneyTransferRequest(
                fromAccountId=source_account.id,
                toAccountId=target_account.id,
                amount=amount,
            ),
        )

        assert (
            transfer_response.json()["error"] == "Amount must be between 500 and 10000"
        ), f"Error: Unexpected error text for a transfer of {amount}"

        source_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, source_account.id
        )
        target_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, target_account.id
        )

        assert source_account_from_db.balance == pytest.approx(
            source_account.balance
        ), f"Error: Source balance changed after a rejected transfer of {amount}"
        assert target_account_from_db.balance == pytest.approx(
            target_account.balance
        ), f"Error: Target balance changed after a rejected transfer of {amount}"

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import (
    AMOUNT_STEP,
    MAX_DEPOSIT_AMOUNT,
    MAX_TRANSFER_AMOUNT,
    MIN_TRANSFER_AMOUNT,
)
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.db.crud.transaction_crud import TransactionCrudDB
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.money_transfer_request import MoneyTransferRequest

DEPOSIT_COUNT = 2


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
    def test_transfer_boundary_money_success(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
        amount: float,
    ):
        source_account = api_manager.user_steps.create_account(create_user_request)
        target_account = api_manager.user_steps.create_account(create_user_request)

        deposit_response = None

        for _ in range(DEPOSIT_COUNT):
            deposit_response = api_manager.user_steps.deposit_account(
                create_user_request,
                DepositRequest(accountId=source_account.id, amount=MAX_DEPOSIT_AMOUNT),
            )

        transfer_response = api_manager.user_steps.transfer_money(
            create_user_request,
            MoneyTransferRequest(
                fromAccountId=source_account.id,
                toAccountId=target_account.id,
                amount=amount,
            ),
        )

        assert transfer_response.fromAccountId == source_account.id, (
            "Error: Wrong source account in the transfer response"
        )
        assert transfer_response.toAccountId == target_account.id, (
            "Error: Wrong target account in the transfer response"
        )
        assert transfer_response.fromAccountIdBalance == pytest.approx(
            deposit_response.balance - amount
        ), "Error: Wrong source balance in the transfer response"

        target_history = api_manager.user_steps.get_account_transactions(
            create_user_request, target_account.id
        )
        assert target_history.balance == pytest.approx(
            target_account.balance + amount
        ), "Error: Target balance in the account history was not increased"

        source_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, source_account.id
        )
        target_account_from_db = AccountCrudDB.get_account_by_id(
            db_session, target_account.id
        )

        assert source_account_from_db is not None, (
            f"Error: Source account {source_account.id} was not found in the database"
        )
        assert target_account_from_db is not None, (
            f"Error: Target account {target_account.id} was not found in the database"
        )
        assert source_account_from_db.balance == pytest.approx(
            deposit_response.balance - amount
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
        transfer_from_db = transfers_from_db[0]
        assert transfer_from_db.to_account_id == target_account.id, (
            "Error: The transfer was saved with a wrong target account"
        )
        assert transfer_from_db.amount == pytest.approx(amount), (
            "Error: The transfer was saved with a wrong amount"
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
    def test_transfer_boundary_money_fail(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
        amount: float,
    ):
        source_account = api_manager.user_steps.create_account(create_user_request)
        target_account = api_manager.user_steps.create_account(create_user_request)

        deposit_response = None

        for _ in range(DEPOSIT_COUNT):
            deposit_response = api_manager.user_steps.deposit_account(
                create_user_request,
                DepositRequest(accountId=source_account.id, amount=MAX_DEPOSIT_AMOUNT),
            )

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

        assert source_account_from_db is not None, (
            f"Error: Source account {source_account.id} was not found in the database"
        )
        assert target_account_from_db is not None, (
            f"Error: Target account {target_account.id} was not found in the database"
        )
        assert source_account_from_db.balance == pytest.approx(
            deposit_response.balance
        ), f"Error: Source balance changed after a rejected transfer of {amount}"
        assert target_account_from_db.balance == pytest.approx(
            target_account.balance
        ), f"Error: Target balance changed after a rejected transfer of {amount}"

        transfers_from_db = TransactionCrudDB.get_transfers_by_from_account_id(
            db_session, source_account.id
        )

        assert transfers_from_db == [], (
            f"Error: A transfer was saved after a rejected transfer of {amount}"
        )

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import (
    AMOUNT_STEP,
    MAX_DEPOSIT_AMOUNT,
    MIN_CREDIT_AMOUNT,
)
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.db.crud.transaction_crud import TransactionCrudDB
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.specs.response_specs import ResponseSpecs

CREDIT_AMOUNT = MIN_CREDIT_AMOUNT
REPAID_CREDIT_DEBT = 0.0


@pytest.mark.api
class TestRepayCredit:
    def test_repay_credit_success(
        self,
        api_manager: ApiManager,
        create_user_request_credit: CreateUserRequest,
        db_session: Session,
    ):
        account, credit = api_manager.user_steps.create_account_with_credit(
            create_user_request_credit, CREDIT_AMOUNT
        )

        credit_repay_response = api_manager.user_steps.repay_credit(
            create_user_request_credit,
            CreditRepayRequest(
                creditId=credit.creditId,
                accountId=account.id,
                amount=CREDIT_AMOUNT,
            ),
        )

        assert credit_repay_response.creditId == credit.creditId, (
            "Error: Wrong credit in the repayment response"
        )
        assert credit_repay_response.amountDeposited == pytest.approx(CREDIT_AMOUNT), (
            "Error: Wrong repaid amount in the repayment response"
        )

        account_from_db = AccountCrudDB.get_account_by_id(db_session, account.id)

        assert account_from_db is not None, (
            f"Error: Account {account.id} was not found in the database"
        )
        assert account_from_db.balance == pytest.approx(
            credit.balance - CREDIT_AMOUNT
        ), "Error: Account balance in the database was not decreased by the repayment"

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit.creditId)

        assert credit_from_db is not None, (
            f"Error: Credit {credit.creditId} was not found in the database"
        )
        assert credit_from_db.balance == pytest.approx(REPAID_CREDIT_DEBT), (
            "Error: The credit debt in the database was not repaid"
        )

        repayments_from_db = TransactionCrudDB.get_repayments_by_credit_id(
            db_session, credit.creditId
        )

        assert len(repayments_from_db) == 1, (
            f"Error: Expected 1 repayment of credit {credit.creditId}, "
            f"got {len(repayments_from_db)}"
        )
        repayment_from_db = repayments_from_db[0]
        assert repayment_from_db.from_account_id == account.id, (
            "Error: The repayment was saved with a wrong account"
        )
        assert repayment_from_db.amount == pytest.approx(CREDIT_AMOUNT), (
            "Error: The repayment was saved with a wrong amount"
        )

    @pytest.mark.parametrize(
        "repay_amount",
        [
            CREDIT_AMOUNT / 2,
            CREDIT_AMOUNT - AMOUNT_STEP,
        ],
        ids=[
            "half_of_credit_amount",
            "credit_amount_minus_one_cent",
        ],
    )
    def test_repay_credit_partial_amount_fails(
        self,
        api_manager: ApiManager,
        create_user_request_credit: CreateUserRequest,
        db_session: Session,
        repay_amount: float,
    ):
        account, credit = api_manager.user_steps.create_account_with_credit(
            create_user_request_credit, CREDIT_AMOUNT
        )

        response = api_manager.user_steps.repay_credit_fail(
            create_user_request_credit,
            CreditRepayRequest(
                creditId=credit.creditId,
                accountId=account.id,
                amount=repay_amount,
            ),
            ResponseSpecs.request_unprocessable_entity(),
        )

        assert (
            response.json()["error"]
            == f"The amount is not enough. Credit balance: {int(-credit.amount)}"
        ), f"Error: Unexpected error text for a repayment of {repay_amount}"

        account_from_db = AccountCrudDB.get_account_by_id(db_session, account.id)

        assert account_from_db is not None, (
            f"Error: Account {account.id} was not found in the database"
        )
        assert account_from_db.balance == pytest.approx(credit.balance), (
            f"Error: Account balance changed after a rejected repayment of {repay_amount}"
        )

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit.creditId)

        assert credit_from_db is not None, (
            f"Error: Credit {credit.creditId} was not found in the database"
        )
        assert credit_from_db.balance == pytest.approx(-CREDIT_AMOUNT), (
            f"Error: Credit debt changed after a rejected repayment of {repay_amount}"
        )

        repayments_from_db = TransactionCrudDB.get_repayments_by_credit_id(
            db_session, credit.creditId
        )

        assert repayments_from_db == [], (
            f"Error: A repayment was saved after a rejected repayment of {repay_amount}"
        )

    def test_repay_credit_overpayment_fails(
        self,
        api_manager: ApiManager,
        create_user_request_credit: CreateUserRequest,
        db_session: Session,
    ):
        account, credit = api_manager.user_steps.create_account_with_credit(
            create_user_request_credit, CREDIT_AMOUNT
        )

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request_credit,
            DepositRequest(
                accountId=account.id,
                amount=MAX_DEPOSIT_AMOUNT,
            ),
        )
        response = api_manager.user_steps.repay_credit_fail(
            create_user_request_credit,
            CreditRepayRequest(
                creditId=credit.creditId,
                accountId=account.id,
                amount=CREDIT_AMOUNT + AMOUNT_STEP,
            ),
            ResponseSpecs.request_unprocessable_entity(),
        )

        assert response.json()["error"] == "Repayment amount exceeds remaining debt", (
            "Error: Unexpected error text for an overpayment"
        )

        account_from_db = AccountCrudDB.get_account_by_id(db_session, account.id)

        assert account_from_db is not None, (
            f"Error: Account {account.id} was not found in the database"
        )
        assert account_from_db.balance == pytest.approx(deposit_response.balance), (
            "Error: Account balance changed after a rejected overpayment"
        )

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit.creditId)

        assert credit_from_db is not None, (
            f"Error: Credit {credit.creditId} was not found in the database"
        )
        assert credit_from_db.balance == pytest.approx(-CREDIT_AMOUNT), (
            "Error: Credit debt changed after a rejected overpayment"
        )

        repayments_from_db = TransactionCrudDB.get_repayments_by_credit_id(
            db_session, credit.creditId
        )

        assert repayments_from_db == [], (
            "Error: A repayment was saved after a rejected overpayment"
        )

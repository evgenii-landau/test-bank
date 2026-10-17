import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.constants import (
    AMOUNT_STEP,
    CREDIT_TERM_MONTHS,
    MAX_CREDIT_AMOUNT,
    MIN_CREDIT_AMOUNT,
)
from src.main.api.db.crud.account_crud import AccountCrudDB
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestRequestCredit:
    @pytest.mark.parametrize(
        "credit_amount",
        [
            MIN_CREDIT_AMOUNT,
            MAX_CREDIT_AMOUNT,
        ],
        ids=[
            "minimum_amount_credit",
            "maximum_amount_credit",
        ],
    )
    def test_request_credit_success(
        self,
        api_manager: ApiManager,
        create_user_request_credit: CreateUserRequest,
        db_session: Session,
        credit_amount: float,
    ):
        account_response = api_manager.user_steps.create_account(
            create_user_request_credit
        )

        credit = api_manager.user_steps.credit_request(
            create_user_request_credit,
            CreditRequest(
                accountId=account_response.id,
                amount=credit_amount,
                termMonths=CREDIT_TERM_MONTHS,
            ),
        )

        assert credit.amount == pytest.approx(credit_amount), (
            "Error: Wrong credit amount in the response"
        )

        account_from_db = AccountCrudDB.get_account_by_id(
            db_session, account_response.id
        )

        assert account_from_db.balance == pytest.approx(
            account_response.balance + credit_amount
        ), "Error: Account balance in the database was not increased by the credit"

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit.creditId)

        assert credit_from_db.balance == pytest.approx(-credit_amount), (
            "Error: The credit debt was not saved as a negative credit amount"
        )

    @pytest.mark.parametrize(
        "credit_amount",
        [
            MIN_CREDIT_AMOUNT - AMOUNT_STEP,
            MAX_CREDIT_AMOUNT + AMOUNT_STEP,
        ],
        ids=[
            "credit_amount_less_than_minimum",
            "credit_amount_greater_than_maximum",
        ],
    )
    def test_request_credit_amount_out_of_range_fails(
        self,
        api_manager: ApiManager,
        create_user_request_credit: CreateUserRequest,
        db_session: Session,
        credit_amount: float,
    ):
        account = api_manager.user_steps.create_account(create_user_request_credit)
        response = api_manager.user_steps.credit_request_fail(
            create_user_request_credit,
            CreditRequest(
                accountId=account.id,
                amount=credit_amount,
                termMonths=CREDIT_TERM_MONTHS,
            ),
            ResponseSpecs.request_bad(),
        )

        assert response.json()["error"] == "Amount must be between 5000 and 15000", (
            f"Error: Unexpected error text for a credit of {credit_amount}"
        )

        credits_from_db = CreditCrudDB.get_credits_by_account_id(db_session, account.id)

        assert credits_from_db == [], (
            f"Error: A credit was saved after a rejected credit of {credit_amount}"
        )

    def test_regular_user_cannot_request_credit(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session,
    ):
        account = api_manager.user_steps.create_account(create_user_request)
        response = api_manager.user_steps.credit_request_fail(
            create_user_request,
            CreditRequest(
                accountId=account.id,
                amount=MIN_CREDIT_AMOUNT,
                termMonths=CREDIT_TERM_MONTHS,
            ),
            ResponseSpecs.request_forbidden(),
        )

        assert response.json()["detail"] == "Forbidden: ROLE_CREDIT access required", (
            "Error: Unexpected error text for a regular user requesting a credit"
        )

        credits_from_db = CreditCrudDB.get_credits_by_account_id(db_session, account.id)

        assert credits_from_db == [], (
            "Error: A credit was saved for a user without the credit role"
        )

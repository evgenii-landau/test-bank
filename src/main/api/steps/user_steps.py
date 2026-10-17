from collections.abc import Callable

from requests import Response

from src.main.api.constants import CREDIT_TERM_MONTHS
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import (
    ValidateCrudRequester,
)
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.money_transfer_request import MoneyTransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    REGULAR_USER_ROLE = "ROLE_USER"
    CREDIT_USER_ROLE = "ROLE_CREDIT_SECRET"

    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            endpoint=Endpoint.ACCOUNT_CREATE,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_created(),
        ).post()

        return response

    def create_account_fail(
        self,
        create_user_request: CreateUserRequest,
        response_spec: Callable[[Response], None],
    ):
        return CrudRequester(
            endpoint=Endpoint.ACCOUNT_CREATE,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=response_spec,
        ).post(None)

    def deposit_account(
        self, create_user_request: CreateUserRequest, deposit_request: DepositRequest
    ):
        response = ValidateCrudRequester(
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).post(deposit_request)

        return response

    def deposit_account_fail(
        self, create_user_request: CreateUserRequest, deposit_request: DepositRequest
    ):
        return CrudRequester(
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_bad(),
        ).post(deposit_request)

    def transfer_money(
        self,
        create_user_request: CreateUserRequest,
        money_transfer_request: MoneyTransferRequest,
    ):
        response = ValidateCrudRequester(
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).post(money_transfer_request)

        return response

    def transfer_money_fail(
        self,
        create_user_request: CreateUserRequest,
        money_transfer_request: MoneyTransferRequest,
    ):
        return CrudRequester(
            endpoint=Endpoint.ACCOUNT_TRANSFER,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_bad(),
        ).post(money_transfer_request)

    def get_account_transactions(
        self, create_user_request: CreateUserRequest, account_id: int
    ):
        response = ValidateCrudRequester(
            endpoint=Endpoint.ACCOUNT_TRANSACTIONS,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).get(account_id)

        return response

    def credit_request(
        self,
        create_user_request_credit: CreateUserRequest,
        credit_request: CreditRequest,
    ):
        response = ValidateCrudRequester(
            endpoint=Endpoint.CREDIT_REQUEST,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request_credit.username,
                password=create_user_request_credit.password,
            ),
            response_spec=ResponseSpecs.request_created(),
        ).post(credit_request)

        return response

    def credit_request_fail(
        self,
        create_user_request: CreateUserRequest,
        credit_request: CreditRequest,
        response_spec: Callable[[Response], None],
    ):
        return CrudRequester(
            endpoint=Endpoint.CREDIT_REQUEST,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=response_spec,
        ).post(credit_request)

    def repay_credit(
        self,
        create_user_request: CreateUserRequest,
        repay_request: CreditRepayRequest,
    ):
        response = ValidateCrudRequester(
            endpoint=Endpoint.CREDIT_REPAY,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=ResponseSpecs.request_ok(),
        ).post(repay_request)

        return response

    def repay_credit_fail(
        self,
        create_user_request: CreateUserRequest,
        repay_request: CreditRepayRequest,
        response_spec: Callable[[Response], None],
    ):
        return CrudRequester(
            endpoint=Endpoint.CREDIT_REPAY,
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password,
            ),
            response_spec=response_spec,
        ).post(repay_request)

    def create_account_with_credit(
        self, create_user_request: CreateUserRequest, credit_amount: float
    ) -> tuple[CreateAccountResponse, CreditResponse]:
        account = self.create_account(create_user_request)
        credit = self.credit_request(
            create_user_request,
            CreditRequest(
                accountId=account.id,
                amount=credit_amount,
                termMonths=CREDIT_TERM_MONTHS,
            ),
        )
        return account, credit

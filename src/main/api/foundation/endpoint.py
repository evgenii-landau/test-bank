from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from src.main.api.models.account_transactions_response import (
    AccountTransactionsResponse,
)
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.money_transfer_request import MoneyTransferRequest
from src.main.api.models.money_transfer_response import MoneyTransferResponse
from src.main.api.models.user_login_request import LoginUserRequest
from src.main.api.models.user_login_response import LoginUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model=None,
        response_model=None,
    )

    LOGIN_USER = EndpointConfiguration(
        url="/auth/token/login",
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
    )

    ACCOUNT_CREATE = EndpointConfiguration(
        url="/account/create",
        request_model=None,
        response_model=CreateAccountResponse,
    )

    ACCOUNT_DEPOSIT = EndpointConfiguration(
        url="/account/deposit",
        request_model=DepositRequest,
        response_model=DepositResponse,
    )

    ACCOUNT_TRANSFER = EndpointConfiguration(
        url="/account/transfer",
        request_model=MoneyTransferRequest,
        response_model=MoneyTransferResponse,
    )

    ACCOUNT_TRANSACTIONS = EndpointConfiguration(
        url="/account/transactions",
        request_model=None,
        response_model=AccountTransactionsResponse,
    )

    CREDIT_REQUEST = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditRequest,
        response_model=CreditResponse,
    )

    CREDIT_REPAY = EndpointConfiguration(
        url="/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse,
    )

from src.main.api.models.base_model import BaseModel
from src.main.api.models.transaction import Transaction


class AccountTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transaction]

from typing import Optional

from src.main.api.models.base_model import BaseModel


class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int]
    toAccountId: Optional[int]
    createdAt: str
    creditId: Optional[int] = None

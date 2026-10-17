from typing import Literal

from src.main.api.models.base_model import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: Literal["ROLE_ADMIN", "ROLE_USER", "ROLE_CREDIT_SECRET"]

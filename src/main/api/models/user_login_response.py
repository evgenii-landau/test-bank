from typing import Literal

from src.main.api.models.base_model import BaseModel


class User(BaseModel):
    username: str
    role: Literal["ROLE_ADMIN", "ROLE_USER", "ROLE_CREDIT_SECRET"]


class LoginUserResponse(BaseModel):
    token: str
    user: User

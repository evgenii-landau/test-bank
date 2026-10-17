from sqlalchemy import Column, Float, ForeignKey, Integer, String

from src.main.api.db.base import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    number = Column(String, nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Account(id: {self.id}, user_id: {self.user_id}, number: {self.number}, balance: {self.balance})>"

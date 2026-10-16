from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDB:
    TRANSFER_TYPE = "transfer"
    CREDIT_REPAYMENT_TYPE = "credit_repayment"

    @staticmethod
    def get_transfers_by_from_account_id(
        db: Session, from_account_id: int
    ) -> list[Transaction]:
        return (
            db.query(Transaction)
            .filter_by(
                from_account_id=from_account_id,
                transaction_type=TransactionCrudDB.TRANSFER_TYPE,
            )
            .all()
        )

    @staticmethod
    def get_repayments_by_credit_id(db: Session, credit_id: int) -> list[Transaction]:
        return (
            db.query(Transaction)
            .filter_by(
                credit_id=credit_id,
                transaction_type=TransactionCrudDB.CREDIT_REPAYMENT_TYPE,
            )
            .all()
        )

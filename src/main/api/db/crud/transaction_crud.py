from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDB:
    TRANSFER_TYPE = "transfer"

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

from sqlalchemy.orm import Session

from src.main.api.db.models.user_table import User


class UserCrudDB:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str) -> User:
        # The server stores a bcrypt hash, so a plain-text password will not log in via the API
        user = User(
            username=username,
            password=password,
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

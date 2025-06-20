from sqlmodel import Session, select
from app.models.user import User
from app.database import engine
from fastapi import HTTPException


def create_user(username: str, role: str) -> tuple[User, str]:
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == username)).first()
        if existing_user:
            existing_user.role = role  # 🔁 Actualizar el rol
            session.add(existing_user)
            session.commit()
            session.refresh(existing_user)
            return existing_user, "updated"

        user = User(username=username, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user, "created"


def get_user_by_username(username: str) -> User | None:
    """ Service to obtain a user by name """
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()

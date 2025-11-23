from sqlalchemy.orm import Session
from typing import Optional
from authentication.models import User
from uuid import uuid4


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter_by(email=email).first()  # type: ignore


def create_user(session: Session, name: str, email: str, password: str):
    new_user = User(id=str(uuid4()), name=name, email=email, password=password)  # type: ignore
    session.add(new_user)
    session.commit()

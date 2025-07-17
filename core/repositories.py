from sqlalchemy.orm import Session
from typing import Optional
from core.models import Article, User
from uuid import uuid4


def get_article_by_id(session: Session, article_id: int) -> Optional[Article]:
    return session.query(Article).filter(Article.id == article_id).first()  # type: ignore


def get_authors_article(
    session: Session,
    article_id: int,
    author_id: str,
) -> Optional[Article]:
    return (
        # type: ignore
        session.query(Article)
        .filter(Article.id == article_id, Article.author == author_id)
        .first()
    )


def get_all_articles(session: Session) -> list[Article]:
    return session.query(Article).all()[::-1]  # type: ignore


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter_by(email=email).first()  # type: ignore


def create_user(session: Session, name: str, email: str, password: str):
    new_user = User(id=str(uuid4()), name=name, email=email, password=password)
    session.add(new_user)
    session.commit()

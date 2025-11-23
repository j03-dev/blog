from sqlalchemy.orm import Session
from typing import Optional
from blog.models import Article, Subscriber
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


def create_subscriber(session: Session, email: str):
    new_subscriber = Subscriber(id=str(uuid4()), email=email)  # type: ignore
    session.add(new_subscriber)
    session.commit()


def get_all_subscribers(session: Session):
    return session.query(Subscriber).all()  # type: ignore

from sqlalchemy.orm import Session

from app.serializers import CredentialSerializer, ArticleSerializer
from app import repositories as repo


def login(session: Session, cred: CredentialSerializer):
    if user := repo.get_user_by_email(session, cred.validated_data["email"]):
        if user.password == cred.validated_data["password"]:
            return user
    return None


def update_article(
    session: Session,
    new_article: ArticleSerializer,
    article_id: int,
    author_id: str,
):
    if article := repo.get_authors_article(session, article_id, author_id):
        return new_article.update(session, article, new_article.validated_data)
    return None


def delete_article(session: Session, article_id: int, author_id: str):
    if article := repo.get_authors_article(session, article_id, author_id):
        session.delete(article)
        session.commit()
        return article
    return None

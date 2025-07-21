from sqlalchemy.orm import Session
from core import repositories as repo
from core.serializers import ArticleSerializer, CredentialSerializer
from core.utils import send_email


def login(session: Session, cred: CredentialSerializer):
    if user := repo.get_user_by_email(session, cred.validated_data["email"]):
        if user.password == cred.validated_data["password"]:
            return user
    return None


def publish_new_article(session: Session, article: ArticleSerializer):
    subscribers = repo.get_all_subscribers(session)
    new_article = article.save(session)
    recipient_emails = [sub.email for sub in subscribers]
    send_email(
        recipient_emails,
        "New Article on Joe's blog",
        f"Title: {new_article.title}",
    )
    return new_article


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

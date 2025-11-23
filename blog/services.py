from sqlalchemy.orm import Session
from blog import repositories as repo
from blog.serializers import ArticleSerializer


def publish_new_article(session: Session, article: ArticleSerializer):
    subscribers = repo.get_all_subscribers(session)
    new_article = article.save(session)
    recipient_emails = [sub.email for sub in subscribers]
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

from oxapy import get, delete, put, post, Request, templating, Status, Redirect
from functools import wraps
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import Optional, Any, Callable, TypeVar, Union

from core.models import Article, User
from core.serializers import (
    ArticleModelSerializer,
    CredentialSerializer,
    ArticleInputSerializer,
)

F = TypeVar("F", bound=Callable[..., Any])
ResponseType = Union[templating.Template, Status, Redirect]


def with_session(func: F) -> F:
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        with Session(request.app_data.engine) as session:  # type: ignore
            return func(request, session, *args, **kwargs)

    return wrapper  # type: ignore


def get_article_with_relations(session: Session, article_id: str) -> Optional[Article]:
    stmt = (
        select(Article)  # type: ignore
        .options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        .where(Article.id == article_id)
    )
    return session.execute(stmt).unique().scalar_one_or_none()


@get("/components/nav")
def nav(request: Request):
    session = request.session()
    is_auth = session.get("is_auth") if session else False
    return templating.render(
        request,
        "components/nav.html.j2",
        {
            "is_auth": is_auth,
        },
    )


@get("/components/article-card/{id}")
@with_session
def card(request: Request, session: Session, id: str):
    article = get_article_with_relations(session, id)
    serializer = ArticleModelSerializer(instance=article)  # type: ignore
    return templating.render(
        request,
        "components/article_card.html.j2",
        {
            "article": serializer.data,
        },
    )


@get("/")
@with_session
def home(request: Request, session: Session):
    articles = session.query(Article).all()  # type: ignore
    serializer = ArticleModelSerializer(instance=articles, many=True)  # type: ignore
    return templating.render(request, "index.html.j2", {"articles": serializer.data})


@get("/articles")
def article_form(request: Request):
    return templating.render(request, "article_form.html.j2")


@post("/articles")
@with_session
def create_article(request: Request, session: Session):
    serializer = ArticleInputSerializer(request.data, context={"request": request})  # type: ignore
    serializer.is_valid()
    serializer.save(session)
    return "Success added"


@get("/articles/{id}")
@with_session
def get_article(request: Request, session: Session, id: str):
    req_session = request.session()
    is_auth = req_session.get("is_auth") if req_session else False
    if article := get_article_with_relations(session, id):
        serializer = ArticleModelSerializer(instance=article)  # type: ignore
        return templating.render(
            request,
            "article.html.j2",
            {
                "article": serializer.data,
                "is_auth": is_auth,
            },
        )

    return templating.render(request, "article.html.j2")


@get("/articles/{id}/edit")
@with_session
def edit_form_article(request: Request, session: Session, id: str):
    article = get_article_with_relations(session, id)
    serializer = ArticleModelSerializer(instance=article)  # type: ignore
    return templating.render(
        request,
        "article_form.html.j2",
        {
            "article": serializer.data,
        },
    )


@put("/articles/{id}")
@with_session
def update_article(request: Request, session: Session, id: int):
    serializer = ArticleInputSerializer(request.data, context={"request": request})  # type: ignore
    serializer.is_valid()
    article = session.query(Article).filter_by(id=id, author=request.user_id).first()  # type: ignore
    serializer.update(article, session)
    return "Article Updated"


@delete("/articles/{id}")
@with_session
def delete_article(request: Request, session: Session, id: int):
    article = session.query(Article).filter_by(id=id, author=request.user_id).first()  # type: ignore
    session.delete(article)
    session.commit()
    return templating.render(request, "article.html.j2")


@get("/login")
def login(request: Request):
    return templating.render(request, "login.html.j2")


@post("/login")
@with_session
def login_form(request: Request, session: Session):
    serializer = CredentialSerializer(request.data)  # type: ignore
    try:
        serializer.is_valid()
        req_session = request.session()
    except Exception as e:
        return templating.render(request, "login.html.j2", {"message": str(e)})

    # type: ignore
    if user := session.query(User).filter_by(**serializer.validate_data).first():
        req_session["user_id"] = user.id
        req_session["is_auth"] = True
        articles = session.query(Article).all()  # type: ignore
        serializer = ArticleModelSerializer(instance=articles, many=True)  # type: ignore
        return templating.render(
            request, "index.html.j2", {"articles": serializer.data}
        )

    return templating.render(
        request,
        "login.html.j2",
        {
            "message": "The Email or Password are False",
        },
    )


@get("/logout")
@with_session
def logout(request: Request, session: Session):
    req_session = request.session()
    req_session.remove("is_auth")
    req_session.remove("user_id")
    articles = session.query(Article).all()  # type: ignore
    serializer = ArticleModelSerializer(instance=articles, many=True)  # type: ignore
    return templating.render(request, "index.html.j2", {"articles": serializer.data})

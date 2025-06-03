from oxapy import get, delete, put, post, Request, templating, Status, Redirect
from functools import wraps
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import Optional, Any, Callable, TypeVar, Union
from urllib.parse import unquote

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


def get_article_with_relations(session: Session, article_id: int) -> Optional[Article]:
    stmt = (
        select(Article)  # type: ignore
        .options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        .where(Article.id == article_id)
    )
    return session.execute(stmt).unique().scalars().first()


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


@get("/components/artciles")
@with_session
def articles(request: Request, session: Session):
    stmt = select(Article).options(  # type: ignore
        joinedload(Article.author_relationship),
        joinedload(Article.images),
    )
    articles = session.execute(stmt).unique().scalars().all()
    serializer = ArticleModelSerializer(instance=articles, many=True)  # type: ignore
    return templating.render(
        request,
        "components/articles.html.j2",
        {
            "articles": serializer.data,
        },
    )


@get("/")
def home(request: Request):
    return templating.render(request, "index.html.j2")


@get("/articles")
def article_form(request: Request):
    return templating.render(request, "article_form.html.j2")


@post("/articles")
@with_session
def create_article(request: Request, session: Session):
    serializer = ArticleInputSerializer(request)  # type: ignore
    serializer.is_valid()
    serializer.save(session)
    return "Success added"


@get("/articles/{id}")
@with_session
def get_article(request: Request, session: Session, id: int):
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
def edit_form_article(request: Request, session: Session, id: int):
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
    serializer = ArticleInputSerializer(request)  # type: ignore
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
    query = request.query()
    message = unquote(query.get("message")) if query else None
    return templating.render(request, "login.html.j2", {"message": message})


@post("/login")
@with_session
def login_form(request: Request, session: Session):
    serializer = CredentialSerializer(request)  # type: ignore
    try:
        serializer.is_valid()
        req_session = request.session()
    except Exception as e:
        return Redirect(f"/login?message={e}")
    # type: ignore
    if user := session.query(User).filter_by(**serializer.validate_data).first():
        req_session["user_id"] = user.id
        req_session["is_auth"] = True
        return Redirect("/")

    return Redirect("/login?message=The Email or Password are False")

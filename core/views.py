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
        with Session(request.app_data.engine) as session:
            return func(request, session, *args, **kwargs)

    return wrapper  # type: ignore


def render_message(
    request: Request,
    success_message: Optional[str] = None,
    failed_message: Optional[str] = None,
) -> templating.Template:
    return templating.render(
        request,
        "message.html.j2",
        {"success_message": success_message, "failed_message": failed_message},
    )


def get_article_with_relations(session: Session, article_id: int) -> Optional[Article]:
    stmt = (
        select(Article)
        .options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        .where(Article.id == article_id)
    )
    return session.execute(stmt).unique().scalars().first()


@get("/nav")
def nav(request: Request) -> templating.Template:
    req_session = request.session()
    return templating.render(
        request,
        "nav.html.j2",
        {
            "is_authenticate": req_session.get("is_authenticate"),
        },
    )


@get("/")
@with_session
def index(request: Request, session: Session) -> templating.Template:
    stmt = select(Article).options(
        joinedload(Article.author_relationship),
        joinedload(Article.images),
    )
    articles = session.execute(stmt).unique().scalars().all()
    serializer = ArticleModelSerializer(instance=articles, many=True)
    req_session = request.session()
    message = request.query()

    return templating.render(
        request,
        "index.html.j2",
        {
            "articles": serializer.data,
            "is_authenticate": req_session.get("is_authenticate"),
            "message": message.get("message") if message else None,
        },
    )


@get("/login")
def login(request: Request) -> templating.Template:
    return templating.render(request, "login.html.j2")


@post("/login")
@with_session
def auth(request: Request, session: Session) -> Union[Redirect, Status]:
    serializer = CredentialSerializer(request)
    serializer.validate()

    if user := session.query(User).filter_by(**serializer.validate_data).first():
        req_session = request.session()
        req_session["user_id"] = user.id
        req_session["is_authenticate"] = True
        return Redirect("/")
    return Status.NOT_FOUND


@get("/article")
def form_article(request: Request) -> templating.Template:
    message = request.query()
    return templating.render(
        request,
        "article_form.html.j2",
        {
            "message": message.get("message") if message else None,
        },
    )


@post("/article")
@with_session
def create_article(request: Request, session: Session) -> templating.Template:
    serializer = ArticleInputSerializer(request)
    serializer.validate()

    new_article = Article(**serializer.validate_data, author=request.user_id)
    session.add(new_article)
    session.commit()

    return render_message(request, success_message="Article Created")


@get("/article/{id}")
@with_session
def retrieve_article(
    request: Request, session: Session, id: int
) -> templating.Template:
    req_session = request.session()
    article = get_article_with_relations(session, id)

    context = {
        "article": ArticleModelSerializer(instance=article).data if article else None,
        "user_id": req_session.get("user_id"),
    }

    return templating.render(request, "article.html.j2", context)


@put("/article/{id}")
@with_session
def update_article(request: Request, session: Session, id: int) -> templating.Template:
    serializer = ArticleInputSerializer(request)
    serializer.validate()

    if article := session.query(Article).filter_by(id=id).first():
        for key, value in serializer.validate_data.items():
            setattr(article, key, value)
        session.commit()
        return render_message(request, success_message="Article Updated")

    return render_message(request, failed_message="Article not Found")


@delete("/article/{id}")
@with_session
def delete_article(request: Request, session: Session, id: int) -> templating.Template:
    if article := session.query(Article).filter_by(id=id).first():
        session.delete(article)
        session.commit()
        return render_message(request, success_message="Article Deleted")

    return render_message(request, failed_message="Article not found")


@post("/logout")
def logout(request: Request) -> Redirect:
    session = request.session()
    session.clear()
    return Redirect("/")


@get("/article/{id}/edit")
@with_session
def edit_article(
    request: Request, session: Session, id: int
) -> Union[templating.Template, Status]:
    article = get_article_with_relations(session, id)

    if not article:
        return Status.NOT_FOUND

    if article.author != request.user_id:
        return Status.FORBIDDEN

    serializer = ArticleModelSerializer(instance=article)
    return templating.render(
        request, "article_form.html.j2", {"article": serializer.data}
    )

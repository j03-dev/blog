from oxapy import get, delete, put, post, Request, templating, Status, Redirect

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from core.models import Article, User
from core.serializers import (
    ArticleModelSerializer,
    CredentialSerializer,
    ArticleInputSerializer,
)


@get("/nav")
def nav(request: Request):
    req_session = request.session()
    return templating.render(
        request,
        "nav.html.j2",
        {
            "is_authenticate": req_session.get("is_authenticate"),
        },
    )


@get("/")
def index(request: Request):
    with Session(request.app_data.engine) as session:
        stmt = select(Article).options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        articles = session.execute(stmt).unique().scalars().all()
        serializer = ArticleModelSerializer(instance=articles, many=True)
        session = request.session()
        message = request.query()
        return templating.render(
            request,
            "index.html.j2",
            {
                "articles": serializer.data,
                "is_authenticate": session.get("is_authenticate"),
                "message": message.get("message") if message else None,
            },
        )


@get("/login")
def login(request: Request):
    return templating.render(request, "login.html.j2")


@post("/login")
def auth(request: Request):
    serializer = CredentialSerializer(request)
    serializer.validate()
    with Session(request.app_data.engine) as session:
        if user := session.query(User).filter_by(**serializer.validate_data).first():
            req_session = request.session()
            req_session["user_id"] = user.id
            req_session["is_authenticate"] = True
            return Redirect("/")
        return Status.NOT_FOUND


@get("/article")
def form_article(request: Request):
    message = request.query()
    return templating.render(
        request,
        "article_form.html.j2",
        {
            "message": message.get("message") if message else None,
        },
    )


@post("/article")
def create_article(request: Request):
    serializer = ArticleInputSerializer(request)
    serializer.validate()
    with Session(request.app_data.engine) as session:
        new_article = Article(
            **serializer.validate_data,
            author=request.user_id
        )
        session.add(new_article)
        session.commit()
    return templating.render(request, "message.html.j2", {"success_message": "Article Created"})


@get("/article/{id}")
def retrieve_article(request: Request, id: int):
    req_session = request.session()
    with Session(request.app_data.engine) as session:
        stmt = (
            select(Article)
            .options(
                joinedload(Article.author_relationship),
                joinedload(Article.images),
            )
            .where(Article.id == id)
        )
        if article := session.execute(stmt).unique().scalars().first():
            serializer = ArticleModelSerializer(instance=article)
            return templating.render(
                request,
                "article.html.j2",
                {
                    "article": serializer.data,
                    "user_id": req_session.get("user_id"),
                },
            )

        return templating.render(
            request,
            "article.html.j2",
            {
                "article": None,
                "user_id": req_session.get("user_id"),
            },
        )


@put("/article/{id}")
def update_article(request: Request, id: int):
    serializer = ArticleInputSerializer(request)
    serializer.validate()
    with Session(request.app_data.engine) as session:
        if article := session.query(Article).filter_by(id=id).first():
            article.title = serializer.validate_data["title"]
            article.content = serializer.validate_data["content"]
            session.commit()
            return templating.render(request, "message.html.j2", {"success_message": "Article Updated"})
        return templating.render(request, "message.html.j2", {"failed_message": "Article not Found"})


@delete("/article/{id}")
def delete_article(request: Request, id: int):
    with Session(request.app_data.engine) as session:
        if article := session.query(Article).filter_by(id=id).first():
            session.delete(article)
            session.commit()
            return templating.render(request, "message.html.j2", {"success_message": "Article Deleted"})
        return templating.render(request, "message.html.j2", {"failed_message": "Article not found"})


@post("/logout")
def logout(request: Request):
    session = request.session()
    session.clear()
    return Redirect("/")


@get("/article/{id}/edit")
def edit_article(request: Request, id: int):
    with Session(request.app_data.engine) as session:
        stmt = (
            select(Article)
            .options(
                joinedload(Article.author_relationship),
                joinedload(Article.images),
            )
            .where(Article.id == id)
        )
        if article := session.execute(stmt).unique().scalars().first():
            if article.author != request.user_id:
                return Status.FORBIDDEN

            serializer = ArticleModelSerializer(instance=article)
            return templating.render(
                request, "article_form.html.j2", {"article": serializer.data}
            )
    return Status.NOT_FOUND

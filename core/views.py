from oxapy import get, put, post, Request, templating, Status, Redirect

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from core.models import Article, User
from core.serializers import (
    ArticleModelSerializer,
    ArticleInputSerializer,
)


@get("/login")
def login(request: Request):
    return templating.render(request, "login.html")


@post("/login")
def auth(request: Request):
    data = request.form()

    with Session(request.app_data.engine) as session:
        if user := session.query(User).filter_by(**data).first():
            req_session = request.session()
            req_session["user_id"] = user.id
            req_session["is_authenticate"] = True
            return Redirect("/")
        return Status.NOT_FOUND


@get("/article")
def article(request: Request):
    return templating.render(request, "article.html")


@get("/article/{id}")
def retrieve_article(request: Request, id: int):
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
            req_session = request.session()
            return templating.render(
                request,
                "article.html",
                {
                    "article": serializer.data,
                    "user_id": req_session.get("user_id"),
                },
            )


@put("/article/{id}")
def update_article(request: Request, id: int):
    with Session(request.app_data.engine) as session:
        article = session.query(Article).filter_by(id=id).first()
        data = request.json()
        article.content = data["content"]
        article.title = data["title"]
        session.commit()
        return "<h1>Arctile modifed</h1>"


@post("/article")
def create_article(request: Request):
    article = ArticleInputSerializer(request)

    try:
        article.validate()
    except Exception as e:
        return str(e), Status.BAD_REQUEST

    with Session(request.app_data.engine) as session:
        new_article = Article(**article.validate_data, author=request.user_id)
        session.add(new_article)
        session.commit()
        return templating.render(request, "article.html", {"message": "success"})


@get("/")
def index(request: Request):
    with Session(request.app_data.engine) as session:
        stmt = select(Article).options(
            joinedload(Article.author_relationship),
            joinedload(Article.images),
        )
        articles = session.execute(stmt).unique().scalars().all()
        serializer = ArticleModelSerializer(instance=articles, many=True)
        return templating.render(request, "index.html", {"articles": serializer.data})


@post("/logout")
def logout(request: Request):
    session = request.session()
    session.clear()
    return Redirect("/")


@get("/article/new")
def new_article(request: Request):
    return templating.render(request, "article_form.html")


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
                request, "article_form.html", {"article": serializer.data}
            )
    return Status.NOT_FOUND

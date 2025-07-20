from oxapy import get, delete, put, post, Request, templating
from sqlalchemy.orm import Session

from core.utils import with_session
from core.serializers import CredentialSerializer, ArticleSerializer
from core import repositories as repo
from core import services as srvs


@get("/components/nav")
def nav(request: Request):
    session = request.session()
    is_auth = session.get("is_auth") if session else False
    return templating.render(
        request,
        "components/nav.html.j2",
        {"is_auth": is_auth},
    )


@get("/components/article-card/{id:int}")
@with_session
def card(request: Request, session: Session, id: int):
    if article := repo.get_article_by_id(session, id):
        serializer = ArticleSerializer(instance=article)  # type: ignore
        return templating.render(
            request,
            "components/article_card.html.j2",
            {"article": serializer.data},
        )
    return templating.render(request, "components/article_card.html.j2")


@get("/")
@with_session
def home(request: Request, session: Session):
    articles = repo.get_all_articles(session)
    serializer = ArticleSerializer(instance=articles, many=True)  # type: ignore
    return templating.render(request, "index.html.j2", {"articles": serializer.data})


@get("/articles")
def article_form(request: Request):
    return templating.render(request, "article_form.html.j2")


@post("/articles")
@with_session
def create_article(request: Request, session: Session):
    serializer = ArticleSerializer(request.data, context={"request": request})  # type: ignore
    serializer.is_valid()
    serializer.save(session)
    return "Success added"


@get("/articles/{id:int}")
@with_session
def get_article(request: Request, session: Session, id: int):
    req_session = request.session()
    is_auth = req_session.get("is_auth") if req_session else False
    if article := repo.get_article_by_id(session, id):
        serializer = ArticleSerializer(instance=article)  # type: ignore
        return templating.render(
            request,
            "article.html.j2",
            {"article": serializer.data, "is_auth": is_auth},
        )

    return templating.render(request, "article.html.j2")


@get("/articles/{id:int}/edit")
@with_session
def edit_form_article(request: Request, session: Session, id: int):
    article = repo.get_article_by_id(session, id)
    serializer = ArticleSerializer(instance=article)  # type: ignore
    return templating.render(
        request,
        "article_form.html.j2",
        {"article": serializer.data},
    )


@put("/articles/{id}")
@with_session
def update_article(request: Request, session: Session, id: int):
    new_article = ArticleSerializer(request.data, context={"request": request})  # type: ignore
    new_article.is_valid()
    srvs.update_article(session, new_article, id, request.user_id)
    return "Article Updated"


@delete("/articles/{id}")
@with_session
def delete_article(request: Request, session: Session, id: int):
    srvs.delete_article(session, id, request.user_id)
    return templating.render(request, "article.html.j2")


@get("/login")
def login(request: Request):
    return templating.render(request, "login.html.j2")


@post("/login")
@with_session
def login_form(request: Request, session: Session):
    req_session = request.session()
    cred = CredentialSerializer(request.data)  # type: ignore
    try:
        cred.is_valid()
    except Exception as e:
        return templating.render(request, "login.html.j2", {"message": str(e)})
    if user := srvs.login(session, cred):
        req_session["user_id"] = user.id
        req_session["is_auth"] = True
        articles = repo.get_all_articles(session)
        serializer = ArticleSerializer(instance=articles, many=True)  # type: ignore
        return templating.render(
            request,
            "index.html.j2",
            {"articles": serializer.data},
        )

    return templating.render(
        request,
        "login.html.j2",
        {"message": "The Email or Password are False"},
    )


@get("/logout")
@with_session
def logout(request: Request, session: Session):
    req_session = request.session()
    req_session.remove("is_auth")
    req_session.remove("user_id")
    articles = repo.get_all_articles(session)
    serializer = ArticleSerializer(instance=articles, many=True)  # type: ignore
    return templating.render(request, "index.html.j2", {"articles": serializer.data})

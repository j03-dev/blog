from oxapy import get, delete, put, post, render, Request

from core.serializers import CredentialSerializer, ArticleSerializer
from core import repositories as repo
from core import services as srvs


@get("/components/nav")
def nav(request: Request):
    session = request.session()
    is_auth = session.get("is_auth") if session else False
    return render(
        request,
        "components/nav.html.j2",
        {"is_auth": is_auth},
    )


@get("/components/article-card/{id:int}")
def card(request: Request, id: int):
    if article := repo.get_article_by_id(request.db, id):
        serializer = ArticleSerializer(instance=article)
        return render(
            request,
            "components/article_card.html.j2",
            {"article": serializer.data},
        )
    return render(request, "components/article_card.html.j2")


@get("/")
def home(request: Request):
    articles = repo.get_all_articles(request.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(request, "index.html.j2", {"articles": serializer.data})


@get("/articles")
def article_form(request: Request):
    return render(request, "article_form.html.j2")


@post("/articles")
def create_article(request: Request):
    serializer = ArticleSerializer(request.data, context={"request": request})
    serializer.is_valid()
    serializer.save(request.db)
    return "Success added"


@get("/articles/{id:int}")
def get_article(request: Request, id: int):
    session = request.session()
    is_auth = session.get("is_auth") if session else False
    if article := repo.get_article_by_id(request.db, id):
        serializer = ArticleSerializer(instance=article)
        return render(
            request,
            "article.html.j2",
            {"article": serializer.data, "is_auth": is_auth},
        )

    return render(request, "article.html.j2")


@get("/articles/{id:int}/edit")
def edit_form_article(request: Request, id: int):
    article = repo.get_article_by_id(request.db, id)
    serializer = ArticleSerializer(instance=article)
    return render(
        request,
        "article_form.html.j2",
        {"article": serializer.data},
    )


@put("/articles/{id}")
def update_article(request: Request, id: int):
    new_article = ArticleSerializer(request.data, context={"request": request})
    new_article.is_valid()
    srvs.update_article(request.db, new_article, id, request.user_id)
    return "Article Updated"


@delete("/articles/{id}")
def delete_article(request: Request, id: int):
    srvs.delete_article(request.db, id, request.user_id)
    return render(request, "article.html.j2")


@get("/login")
def login(request: Request):
    return render(request, "login.html.j2")


@post("/login")
def login_form(request: Request):
    session = request.session()
    cred = CredentialSerializer(request.data)
    try:
        cred.is_valid()
    except Exception as e:
        return render(request, "login.html.j2", {"message": str(e)})
    if user := srvs.login(request.db, cred):
        session["user_id"] = user.id
        session["is_auth"] = True
        articles = repo.get_all_articles(request.db)
        serializer = ArticleSerializer(instance=articles, many=True)
        return render(
            request,
            "index.html.j2",
            {"articles": serializer.data},
        )

    return render(
        request,
        "login.html.j2",
        {"message": "The Email or Password are False"},
    )


@get("/logout")
def logout(request: Request):
    session = request.session()
    session.remove("is_auth")
    session.remove("user_id")
    articles = repo.get_all_articles(request.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(request, "index.html.j2", {"articles": serializer.data})

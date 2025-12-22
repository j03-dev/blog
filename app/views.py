from oxapy import Request, render, get, post, put, delete


from app.serializers import CredentialSerializer, ArticleSerializer
from app import repositories as repo
from app import services as srvs


@get("/")
def home(req: Request):
    articles = repo.get_all_articles(req.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(req, "index.html.j2", {"articles": serializer.data})


@get("/about")
def about(req: Request):
    return render(req, "about.html.j2")


@get("/login")
def login_form(req: Request):
    return render(req, "login.html.j2")


@post("/login")
def authenticate_user(req: Request):
    session = req.session
    cred = CredentialSerializer(req.data)
    try:
        cred.is_valid()
    except Exception as e:
        return render(req, "login.html.j2", {"message": str(e)})
    if user := srvs.login(req.db, cred):
        session["user_id"] = user.id
        session["is_auth"] = True
        articles = repo.get_all_articles(req.db)
        serializer = ArticleSerializer(instance=articles, many=True)
        return render(
            req,
            "index.html.j2",
            {"articles": serializer.data},
        )

    return render(
        req,
        "login.html.j2",
        {"message": "The Email or Password are False"},
    )


@get("/logout")
def logout(req: Request):
    req.session.clear()
    articles = repo.get_all_articles(req.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(req, "index.html.j2", {"articles": serializer.data})


@get("/components/nav")
def nav(req: Request):
    is_auth = req.session.get("is_auth") or False
    return render(
        req,
        "components/nav.html.j2",
        {"is_auth": is_auth},
    )


@get("/components/article-card/{id:int}")
def card(req: Request, id: int):
    if article := repo.get_article_by_id(req.db, id):
        serializer = ArticleSerializer(instance=article)
        return render(
            req,
            "components/article_card.html.j2",
            {"article": serializer.data},
        )
    return render(req, "components/article_card.html.j2")


@get("/articles")
def article_form(req):
    return render(req, "article_form.html.j2")


@post("/articles")
def create_article(req: Request):
    serializer = ArticleSerializer(req.data, context={"req": req})
    serializer.is_valid()
    serializer.save(req.db)
    return "Success added"


@get("/articles/{id:int}")
def get_article(req: Request, id: int):
    is_auth = req.session.get("is_auth") or False
    if article := repo.get_article_by_id(req.db, id):
        serializer = ArticleSerializer(instance=article)
        return render(
            req,
            "article.html.j2",
            {"article": serializer.data, "is_auth": is_auth},
        )

    return render(req, "article.html.j2")


@get("/articles/{id:int}/edit")
def edit_form_article(req, id):
    article = repo.get_article_by_id(req.db, id)
    serializer = ArticleSerializer(instance=article)
    return render(
        req,
        "article_form.html.j2",
        {"article": serializer.data},
    )


@put("/articles/{id:int}")
def update_article(req: Request, id:int):
    new_article = ArticleSerializer(req.data, context={"req": req})
    new_article.is_valid()
    srvs.update_article(req.db, new_article, id, req.user_id)
    return "Article Updated"


@delete("/articles/{id:int}")
def delete_article(req: Request, id: int):
    srvs.delete_article(req.db, id, req.user_id)
    return render(req, "article.html.j2")

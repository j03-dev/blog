from oxapy import (
    Request,
    Redirect,
    Status,
    render,
    get,
    post,
    put,
    delete,
    catcher,
    Response,
)

from app.serializers import CredentialSerializer, ArticleSerializer
from app import repositories as repo
from app import services


@get("/")
def home(req: Request):
    articles = repo.get_all_articles(req.db)
    article_serializer = ArticleSerializer(instance=articles, many=True)
    return render(req, "index.html.j2", {"articles": article_serializer.data})


@get("/about")
def about(req: Request):
    return render(req, "about.html.j2")


@get("/login")
def login_form(req: Request):
    return render(req, "login.html.j2")


@post("/login")
def authenticate_user(req: Request):
    try:
        cred = CredentialSerializer(req.data)
        cred.is_valid()
    except Exception as e:
        return render(req, "components/alert.html.j2", {"error": str(e)})
    if user := services.login(req.db, cred):
        session = req.session
        session["user_id"] = user.id
        session["is_auth"] = True
        response = Response("", content_type="text/plain")
        response.insert_header("HX-Redirect", "/")
        return response
    return render(
        req, "components/alert.html.j2", {"error": "The Email or Password are False"}
    )


@get("/logout")
def logout(req: Request):
    req.session.clear()
    articles = repo.get_all_articles(req.db)
    article_serializer = ArticleSerializer(instance=articles, many=True)
    return render(req, "index.html.j2", {"articles": article_serializer.data})


@get("/components/nav")
def nav(req: Request):
    is_auth = req.session.get("is_auth") or False
    return render(req, "components/nav.html.j2", {"is_auth": is_auth})


@get("/articles")
def article_form(req):
    return render(req, "article_form.html.j2")


@post("/articles")
def create_article(req: Request):
    article_serializer = ArticleSerializer(req.data, context={"req": req})
    article_serializer.is_valid()
    article_serializer.save(req.db)
    return "Success added"


@get("/articles/{article_id:int}")
def get_article(req: Request, article_id: int):
    is_auth = req.session.get("is_auth") or False
    if article := repo.get_article_by_id(req.db, article_id):
        article_serializer = ArticleSerializer(instance=article)
        return render(
            req,
            "article.html.j2",
            {"article": article_serializer.data, "is_auth": is_auth},
        )
    return render(req, "article.html.j2")


@get("/articles/{article_id:int}/edit")
def edit_form_article(req, article_id: int):
    article = repo.get_article_by_id(req.db, article_id)
    article_serializer = ArticleSerializer(instance=article)
    return render(req, "article_form.html.j2", {"article": article_serializer.data})


@put("/articles/{article_id:int}")
def update_article(req: Request, article_id: int):
    new_article = ArticleSerializer(req.data, context={"req": req})
    new_article.is_valid()
    services.update_article(req.db, new_article, article_id, req.user_id)
    return "Article Updated"


@delete("/articles/{article_id:int}")
def delete_article(req: Request, article_id: int):
    services.delete_article(req.db, article_id, req.user_id)
    return render(req, "article.html.j2")


@catcher(Status.NOT_FOUND)
def not_found_page(req: Request, _resp: Response):
    return render(req, "not_found.html.j2")

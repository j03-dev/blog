from oxapy import Request, render
from blog.serializers import ArticleSerializer
from blog import repositories as repo
from blog import services as srvs


def nav(request: Request):
    session = request.session()
    is_auth = session.get("is_auth") if session else False
    return render(
        request,
        "components/nav.html.j2",
        {"is_auth": is_auth},
    )


def card(request: Request, id: int):
    if article := repo.get_article_by_id(request.db, id):
        serializer = ArticleSerializer(instance=article)
        return render(
            request,
            "components/article_card.html.j2",
            {"article": serializer.data},
        )
    return render(request, "components/article_card.html.j2")


def home(request: Request):
    articles = repo.get_all_articles(request.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(request, "index.html.j2", {"articles": serializer.data})


def article_form(request: Request):
    return render(request, "article_form.html.j2")


def create_article(request: Request):
    serializer = ArticleSerializer(request.data, context={"request": request})
    serializer.is_valid()
    serializer.save(request.db)
    return "Success added"


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


def edit_form_article(request: Request, id: int):
    article = repo.get_article_by_id(request.db, id)
    serializer = ArticleSerializer(instance=article)
    return render(
        request,
        "article_form.html.j2",
        {"article": serializer.data},
    )


def update_article(request: Request, id: int):
    new_article = ArticleSerializer(request.data, context={"request": request})
    new_article.is_valid()
    srvs.update_article(request.db, new_article, id, request.user_id)
    return "Article Updated"


def delete_article(request: Request, id: int):
    srvs.delete_article(request.db, id, request.user_id)
    return render(request, "article.html.j2")


def about(request: Request):
    return render(request, "about.html.j2")

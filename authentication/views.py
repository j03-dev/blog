from oxapy import Request, render
from authentication.serializers import CredentialSerializer
from authentication import services as srvs
from blog import repositories as blog_repo
from blog.serializers import ArticleSerializer


def login_page(request: Request):
    return render(request, "login.html.j2")


def login(request: Request):
    session = request.session()
    cred = CredentialSerializer(request.data)
    try:
        cred.is_valid()
    except Exception as e:
        return render(request, "login.html.j2", {"message": str(e)})
    if user := srvs.login(request.db, cred):
        session["user_id"] = user.id
        session["is_auth"] = True
        articles = blog_repo.get_all_articles(request.db)
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


def logout(request: Request):
    session = request.session()
    session.remove("is_auth")
    session.remove("user_id")
    articles = blog_repo.get_all_articles(request.db)
    serializer = ArticleSerializer(instance=articles, many=True)
    return render(request, "index.html.j2", {"articles": serializer.data})

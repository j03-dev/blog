from django.shortcuts import render, get_object_or_404

from core.models import Article


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def index(request):
    return render(request, "index.html", {"all_article": Article.objects.all()})


def post(request, pk: int):
    article = get_object_or_404(Article, id=pk)
    return render(request, "post.html", {"article": article})

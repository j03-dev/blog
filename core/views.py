from django.shortcuts import render, get_object_or_404

from core.models import Article
from .forms import ContactForm


def about(request):
    return render(request, "about.html")


def contact(request):
    message = None
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = "success"
            form.save()
        else:
            message = "failed"

    return render(request, "contact.html", {"message": message})


def index(request):
    articles = Article.objects.all()
    return render(request, "index.html", {"all_article": articles})


def post(request, pk: int):
    article = get_object_or_404(Article, id=pk)
    return render(request, "post.html", {"article": article})

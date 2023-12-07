from django.urls import path

from .views import index, about, contact, post

urlpatterns = [
    path("", index),
    path("about/", about),
    path("contact/", contact),
    path("post/<int:pk>", post),
]

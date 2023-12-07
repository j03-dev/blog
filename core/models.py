from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, null=False)
    image = models.ImageField()
    content = models.TextField(null=False)
    date = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Image(models.Model):
    path = models.ImageField()


class Contact(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(null=False)
    message = models.TextField(null=False)
    date = models.DateTimeField(auto_now=True)

from django.db import models
from utils.models.mixins import TimeStampedMixin

class Post(TimeStampedMixin):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)


class Comment(TimeStampedMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)


class User(TimeStampedMixin):
    name = models.CharField(max_length=10)

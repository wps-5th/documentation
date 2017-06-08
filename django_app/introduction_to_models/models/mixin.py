from django.db import models
from utils.models.mixins import TimeStampedMixin


class Post(TimeStampedMixin):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    like_users = models.ManyToManyField(
        'User',
        related_name='like_posts',
        through='PostLike',
    )


class Comment(TimeStampedMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey('User')
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = 'introduction_to_models_post_like_users'


class User(TimeStampedMixin):
    name = models.CharField(max_length=10)


class Tag(models.Model):
    title = models.CharField(max_length=50)

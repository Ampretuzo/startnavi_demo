from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        db_table = "medium_user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "medium_user_profile"


class Post(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "medium_post"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "medium_post_like"

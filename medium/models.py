from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


from .exceptions import PostAlreadyLiked, LikeNotFound


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

    def like(self, user_profile):
        if self.like_set.count() > 0:
            raise PostAlreadyLiked()
        self.like_set.create(user_profile=user_profile)

    def unlike(self, user_profile):
        if self.like_set.count() == 0:
            raise LikeNotFound()
        self.like_set.filter(user_profile=user_profile).delete()

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        return request.user.is_authenticated

    @staticmethod
    def has_like_permission(request):
        return True

    def has_object_like_permission(self, request):
        return request.user.is_authenticated

    @staticmethod
    def has_unlike_permission(request):
        return True

    def has_object_unlike_permission(self, request):
        return request.user.is_authenticated

    class Meta:
        db_table = "medium_post"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "medium_post_like"

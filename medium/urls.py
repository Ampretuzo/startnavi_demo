from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import UserCreateView as DjoserUserCreateView

from . import views


post_view = views.PostModelViewSet.as_view({"get": "list", "post": "create"})
like_view = views.PostModelViewSet.as_view({"post": "like"})
unlike_view = views.PostModelViewSet.as_view({"post": "unlike"})


urlpatterns = [
    path("auth/register/", DjoserUserCreateView.as_view(), name="register"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("posts/<int:pk>/like/", like_view, name="post-like"),
    path("posts/<int:pk>/unlike/", unlike_view, name="post-unlike"),
    path("posts/", post_view, name="post-list"),
]

"""starnavi_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from medium import views as medium_views


post_view = medium_views.PostModelViewSet.as_view({"get": "list", "post": "create"})
like_view = medium_views.PostModelViewSet.as_view({"post": "toggle_like"})

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/posts/<int:pk>/like/", like_view, name="toggle-like"),
    path("api/posts/", post_view, name="post-list"),
]

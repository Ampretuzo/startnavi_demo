from rest_framework import generics
from rest_framework import permissions

from . import models
from .serializers import PostSerializer


class PostListCreate(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user.userprofile)

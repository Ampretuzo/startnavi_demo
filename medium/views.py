from rest_framework import viewsets

from dry_rest_permissions.generics import DRYPermissions


from . import models
from .serializers import PostSerializer


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (DRYPermissions,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user.userprofile)

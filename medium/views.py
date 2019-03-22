from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import detail_route

from dry_rest_permissions.generics import DRYPermissions


from . import models
from .serializers import PostSerializer


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (DRYPermissions,)

    @detail_route(methods=("POST",))
    def toggle_like(self, request, pk):
        post = self.get_object()
        raise NotImplementedError("Liking a post is not implemented")

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user.userprofile)

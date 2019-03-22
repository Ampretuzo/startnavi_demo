from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status

from dry_rest_permissions.generics import DRYPermissions


from . import models
from .serializers import PostSerializer
from .exceptions import PostAlreadyLiked


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (DRYPermissions,)

    # @detail_route(methods=("POST",))
    def like(self, request, pk):
        post = self.get_object()
        user = self.request.user
        try:
            post.like(user_profile=user.userprofile)
        except PostAlreadyLiked as post_liked_exception:
            # TODO: could return some meaningful response data
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()

    # @detail_route(methods=("POST",))
    def unlike(self, request, pk):
        post = self.get_object()
        raise NotImplementedError("Unlike not implemented")

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user.userprofile)

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "text", "author", "created")

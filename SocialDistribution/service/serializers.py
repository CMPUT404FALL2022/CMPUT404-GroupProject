from rest_framework import serializers
from authors.models import single_author
from post.models import Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = single_author
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
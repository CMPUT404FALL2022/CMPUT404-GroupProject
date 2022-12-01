from rest_framework import serializers
from authors.models import single_author, Followers
from post.models import Post, Comment, Like
import uuid


class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.CharField(default='author', max_length=10)

    class Meta:
        model = single_author
        fields = ('type','id','url','host','github','profileImage','username')

class PostsSerializer(serializers.ModelSerializer):

    type = serializers.CharField(max_length=10,default='posts')

    class Meta:
        model = Post
        fields = ('uuid','type','title','id','source','description','contentType','content','author','Categories','count','origin','published','visibility','unlisted')

class ImagePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_image',)

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uuid','type','author','comment','contentType','published','id')

# class followSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Followers
#         fields = 'all'

class likedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('type','summary','author','object')
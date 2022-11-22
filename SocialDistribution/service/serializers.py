from rest_framework import serializers
from authors.models import single_author
from post.models import Post


class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.CharField(default='author', max_length=10)
    
    class Meta:
        model = single_author
        fields = ('type','id','url','host','display_name','github','profileImage')

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
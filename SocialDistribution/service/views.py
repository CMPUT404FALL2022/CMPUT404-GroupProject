from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import AuthorSerializer, PostsSerializer
from authors.models import single_author
from post.models import Post
from django.db.models import Q

import uuid

"""
Authors and Single Author
"""
@api_view(['GET'])
def authorsList(request):
    authors = single_author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def singleAuthor(request,pk):

    if request.method == 'GET':
        author = single_author.objects.get(id = pk)
        serializer = AuthorSerializer(author, many=False)

    #Update
    if request.method == 'POST':
        author = single_author.objects.get(id = pk)
        serializer = AuthorSerializer(instance = author, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    return Response(serializer.data)

"""
Posts
"""
@api_view(['GET','POST'])
def Posts(request,pk):

    if request.method == 'GET':
        author = single_author.objects.get(id = pk)
        posts = Post.objects.filter(author = author)
        serializer = PostsSerializer(posts, many=True)
    
    #Create new posts
    if request.method == 'POST':
        serializer = PostsSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    return Response(serializer.data)

"""
Wrote but not tested yet!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
@api_view(['GET','POST','DELETE','PUT'])
def getPost(request,pk,postsId):
    if request.method == 'GET':
        author = single_author.objects.get(id = pk)
        posts = Post.objects.get(Q(author = author) & Q(uuid = postsId))
        serializer = PostsSerializer(posts, many=True)

        return Response(serializer.data)
    
    #Update post
    elif request.method == 'POST':
        author = single_author.objects.get(id = pk)
        posts = Post.objects.get(Q(author = author) & Q(uuid = postsId))
        serializer = PostsSerializer(instance = posts, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        author = single_author.objects.get(id = pk)
        posts = Post.objects.get(Q(author = author) & Q(uuid =postsId))
        posts.delete()

        return Response("Post deleted successfully!")

    elif request.method == 'PUT':
        request.data.uuid = postsId
        serializer = PostsSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)







    


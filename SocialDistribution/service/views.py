from django.http import HttpResponseRedirect,FileResponse
from django.shortcuts import render
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import AuthorSerializer, PostsSerializer, ImagePostsSerializer
from authors.models import single_author
from post.models import Post
from django.db.models import Q
"""
Authors and Single Author
"""
@api_view(['GET'])
def authorsList(request):
    """
    This view is used to display all authors information
    """
    authors = single_author.objects.all()
    itemsList = []

    #Hand write pagination
    #Get page and size
    try:
        absURL = request.build_absolute_uri()
        value = absURL.split('?')[1].split('&')
        page = int(value[0].split('=')[1])
        size = int(value[1].split('=')[1])
        fromNum = page * size - size
        toNum = page * size

        authors = authors[fromNum:toNum]

        for item in authors:
            serializer = AuthorSerializer(item)
            data = serializer.data
            itemsList.append(data)

        responseData = {
            "type":"authors",
            "items":itemsList
        }

    except:
        for item in authors:
            serializer = AuthorSerializer(item)
            data = serializer.data
            itemsList.append(data)

        responseData = {
            "type":"authors",
            "items":itemsList
        }

    return Response(responseData,status=200)

@api_view(['GET','POST'])
def singleAuthor(request,pk):
    """
    This view is used to display and update one author information
    """
    if request.method == 'GET':
        #if this author exists, then serialize it, otherwise return 404 not found
        try:
            author = single_author.objects.get(uuid = pk)
        except:
            return Response(status=404)

        serializer = AuthorSerializer(author, many=False)

    #Update
    if request.method == 'POST':
        author = single_author.objects.get(uuid = pk)
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
    """
    This view is used to display posts of a given author and create a new post
    """

    if request.method == 'GET':
        author = single_author.objects.get(uuid = pk)
        posts = Post.objects.filter(author = author)
        serializer = PostsSerializer(posts, many=True)
    
    #Create new posts
    if request.method == 'POST':
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        else:
            return Response(status=400)


    return Response(serializer.data)

"""
POST Manipulation
"""
@api_view(['GET','DELETE','POST','PUT'])
def getPost(request,pk,postsId):
    if request.method == 'GET':
        posts = Post.objects.filter(uuid = postsId)
        serializer = PostsSerializer(posts, many=True)

        return Response(serializer.data)
    
    #Update existing post
    elif request.method == 'POST':

        author = single_author.objects.get(uuid = pk)

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"),status=303)

        posts = Post.objects.get(Q(author = author) & Q(uuid = postsId))
        serializer = PostsSerializer(instance = posts, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    #Delete the post
    elif request.method == 'DELETE':
        author = single_author.objects.get(id = pk)
        posts = Post.objects.get(Q(author = author) & Q(uuid =postsId))
        posts.delete()

        return Response(status=200)

    #Create a new post
    elif request.method == 'PUT':
        if not Post.objects.filter(uuid = postsId).exists():
            serializer = PostsSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data,status=200)

"""
Image Posts
"""
@api_view(['GET'])
def getImage(request,pk,postsId):
    """
    This is in order to display the image post or the image in the post
    """

    if request.method == 'GET':
        try:
            imagePath = '.'+Post.objects.get(uuid = postsId).post_image.url
        except:
            return Response(status=404)
        
        img = open(imagePath, 'rb')

    return FileResponse(img)






    


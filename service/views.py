from django.http import HttpResponseRedirect,FileResponse
from django.shortcuts import render
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import permissions,authentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from .serializers import AuthorSerializer, PostsSerializer, ImagePostsSerializer
from .serializers import commentSerializer
from authors.models import single_author, Followers
from post.models import Post, Comment
from django.db.models import Q


def pagination(request,object):
    """
    This function is hand write pagination method, to get the page and size of user want,
    that returns the range of objects to them
    """
    absURL = request.build_absolute_uri()
    value = absURL.split('?')[1].split('&')
    page = int(value[0].split('=')[1])
    size = int(value[1].split('=')[1])
    fromNum = page * size - size
    toNum = page * size

    object = object[fromNum:toNum]

    return object

"""
Authors and Single Author
"""
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def authorsList(request):
    """
    This view is used to display all authors information
    """
    authors = single_author.objects.all()
    itemsList = []

    #Hand write pagination
    #Get page and size
    try:
        authors = pagination(request,authors)

        if not authors.exists():
            return Response(status=404)

        for item in authors:
            print(item)
            dict = {}
            serializer = AuthorSerializer(item)
            data = serializer.data

            for k,v in data.items():
                dict[k] = v
            
            # dict['displayName'] = 

            itemsList.append(dict)

        responseData = {
            "type":"authors",
            "items":itemsList
        }

    except:
        for item in authors:
            dict = {}
            serializer = AuthorSerializer(item)
            data = serializer.data

            for k,v in data.items():
                dict[k] = v
            
            dict['displayName'] = data['username']
            dict.pop('username')

            itemsList.append(dict)

        responseData = {
            "type":"authors",
            "items":itemsList
        }

    return Response(responseData,status=200)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def singleAuthor(request,pk):
    """
    This view is used to display and update one author information
    """
    if request.method == 'GET':
        #if this author exists, then serialize it, otherwise return 404 not found
        try:
            author = single_author.objects.get(uuid = pk)
            serializeAuthor = AuthorSerializer(author)
            data = serializeAuthor.data
            dict = {}

            for k,v in data.items():
                dict[k] = v
            
            dict['displayName'] = data['username']
            dict.pop('username')

            responseData = {
                "type":"authors",
                "items":dict
            }

            return Response(responseData,status=200)
                
        except:
            return Response(status=404)

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
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def getAllPublicPosts(request):
    """
    This view will get all public posts
    """
    if request.method == 'GET':
        item_list = []

        posts = Post.objects.filter(unlisted = False, visibility = 'PUBLIC')
        for item in posts:
            dict = {}
            serializer = PostsSerializer(item)
            data = serializer.data
            for k,v in data.items():
                dict[k] = v
                print(k,v)
            
            authorUsername = data['author']
            author = single_author.objects.get(username=authorUsername)
            serializeAuthor = AuthorSerializer(author)
            categories = data['Categories']
            catList = categories.split(' ')
            postsId = data['uuid']
            comment = Comment.objects.filter(post__uuid = postsId)
            count = len(comment)
            commentURL = request.build_absolute_uri()+postsId+'/comments'
            dict.pop('Categories')
            dict['categories'] = catList
            dict['author'] = serializeAuthor.data
            dict['comments'] = commentURL
            dict['count'] = count
            item_list.append(dict)

        responseData = {
        "type":"posts",
        "items":item_list
        }
    
    return Response(responseData,status=200)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def Posts(request,pk):
    """
    This view is used to display posts of a given author and create a new post
    """

    if request.method == 'GET':
        item_list = []

        author = single_author.objects.get(uuid = pk)

        serializeAuthor = AuthorSerializer(author)
        try:
            
            posts = Post.objects.filter(author = author)

            posts = pagination(request,posts)

            if not posts.exists():
                return Response(status=404)
            
            for item in posts:
                dict = {}
                serializer = PostsSerializer(item)
                data = serializer.data
                author_dict = {}
                for k,v in data.items():
                    dict[k] = v
                for k,v in serializeAuthor.data.items():
                    author_dict[k] = v
                author_dict['displayName'] = serializeAuthor.data['username']
                author_dict.pop('username')
                categories = data['Categories']
                catList = categories.split(' ')
                postsId = data['uuid']
                comment = Comment.objects.filter(post__uuid = postsId)
                count = len(comment)
                commentURL = request.build_absolute_uri()+postsId+'/comments'
                dict.pop('Categories')
                dict['categories'] = catList
                dict['author'] = author_dict
                dict['comments'] = commentURL
                dict['count'] = count
                item_list.append(dict)

            responseData = {
            "type":"posts",
            "items":item_list
            }

        except: 
            for item in posts:
                dict = {}
                serializer = PostsSerializer(item)
                data = serializer.data
                author_dict = {}
                for k,v in data.items():
                    dict[k] = v
                for k,v in serializeAuthor.data.items():
                    author_dict[k] = v
                author_dict['displayName'] = serializeAuthor.data['username']
                author_dict.pop('username')
                categories = data['Categories']
                catList = categories.split(' ')
                postsId = data['uuid']
                comment = Comment.objects.filter(post__uuid = postsId)
                count = len(comment)
                commentURL = request.build_absolute_uri()+postsId+'/comments'
                dict.pop('Categories')
                dict['categories'] = catList
                dict['author'] = author_dict
                dict['comments'] = commentURL
                dict['count'] = count
                item_list.append(dict)

            responseData = {
            "type":"posts",
            "items":item_list
            }
        
        return Response(responseData,status=200)

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
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def getPost(request,pk,postsId):
    """
    Get a specific post details
    """
    if request.method == 'GET':
        posts = Post.objects.filter(uuid = postsId)
        serializer = PostsSerializer(posts[0])
        author = single_author.objects.get(uuid = pk)
        serializeAuthor = AuthorSerializer(author)
        data = serializer.data
        dict = {}
        for k,v in data.items():
            dict[k] = v
        author_dict = {}
        author_data = serializeAuthor.data
        for k,v in author_data.items():
            author_dict[k] = v
        author_dict['displayName'] = author_data['username']
        author_dict.pop('username')
        categories = data['Categories']
        catList = categories.split(' ')
        postsId = data['uuid']
        comment = Comment.objects.filter(post__uuid = postsId)
        count = len(comment)
        commentURL = request.build_absolute_uri()+postsId+'/comments'
        dict.pop('Categories')
        dict['categories'] = catList
        dict['author'] = author_dict
        dict['comments'] = commentURL
        dict['count'] = count
        
        return Response(dict,status=200)
    
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
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
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

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def getComments(request,pk,postsId):
    """
    Get comments for a post and paginated
    """
    if request.method == 'GET':
        item_list = []
        comments = Comment.objects.filter(post__uuid = postsId)

        try:
            comments = pagination(request,comments)

            for item in comments:
                serializer = commentSerializer(item)
                data = serializer.data
                dict = {}
                for k,v in data.items():
                    dict[k]=v
                
                author = single_author.objects.get(username = data['author'])
                serializeAuthor = AuthorSerializer(author)
                dict['author'] = serializeAuthor.data
                item_list.append(dict)
            
            responseData = {
            "type":'comments',
            "items":item_list
            }

            return Response(responseData,status=200)
        except:
            for item in comments:
                dict = {}
                serializer = commentSerializer(item)
                data = serializer.data
                for k,v in data.items():
                    dict[k]=v
                
                author = single_author.objects.get(username = data['author'])
                serializeAuthor = AuthorSerializer(author)
                dict['author'] = serializeAuthor.data
                data= serializeAuthor.data
                author_dict = {}
                for k,v in data.items():
                    author_dict[k] = v
                
                author_dict['displayName'] = data['username']
                author_dict.pop('username')
                dict['author'] = author_dict
                item_list.append(dict)
            
            responseData = {
            "type":'comments',
            "items":item_list
            }

            return Response(responseData,status=200)

    elif request.method == 'POST':

        serializer = commentSerializer(data=request.data)

        if serializer.is_valid():
            post = Post.objects.get(uuid=postsId)
            serializer.save(post=post)

        else:
            return Response(status=400)

        return Response(serializer.data,status=200)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def getFollowers(request,pk):
    """
    Display a list of followers that followed by user<pk>
    """
    if request.method == 'GET':
        oneFollowers = Followers.objects.filter(follower__uuid=pk)

        followerList = []

        for followers in oneFollowers:
            serializer = AuthorSerializer(followers.author, many=False)
            followerList.append(serializer.data)

        data = {
            "type": "followers",
            "items":followerList,
        }

        return Response(data,status=200)

@api_view(['DELETE','PUT','GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.BasicAuthentication])
def oneFollower(request,pk,foreignPk):
    """
    Execute<br>
    DELETE: delete the author<foreignPk> from author<pk>'s follower list<br>
    PUT: add a new author<foreignPk> to the author<pk>'s follower list<br>
    GET: if author<foreignPk> followed author<pk>, author details will be displayed

    """

    if request.method == 'DELETE':  
        selectedFollowObject = Followers.objects.filter(Q(follower__uuid=pk)&Q(author__uuid = foreignPk))
        selectedFollowObject.delete()
        return Response(status=200)

    elif request.method == 'PUT':
        """
        Followers author ---follows----> follwer
                  author is a follower of follower

        add foreignPk --> follower.author
        add pk --> follower.follower
        """
        currentUserName = single_author.objects.get(uuid = foreignPk).username

        if request.user.is_authenticated:
            followedBy = single_author.objects.get(uuid = foreignPk)
            followTo = single_author.objects.get(uuid = pk)
            newFollow  = Followers(author = followedBy,follower = followTo)
            newFollow.save()
            return Response(status=200)

        else:
            return HttpResponseRedirect(reverse("login"),status=303)


    elif request.method == 'GET':
        
        selectedFollowObject = Followers.objects.filter(Q(follower__uuid=pk)&Q(author__uuid = foreignPk))

        if selectedFollowObject.exists():
        
            selectedFollower = single_author.objects.filter(uuid = foreignPk)
            serializer = AuthorSerializer(selectedFollower,many=True)
            data = {"isFollowed":True,
                    "author":serializer.data}

            return Response(data,status = 200)

        else:
            return Response({
                "isFollowed":False,
            },status=404)
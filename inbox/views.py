from django.shortcuts import render
from authors.models import single_author
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from .models import InboxItem
from post.models import Liked, Like, Post, Comment
from .models import Inbox
from authors.models import FollowRequest
from django.db.models import Q


@login_required(login_url='/login/')
def my_inbox(request,userId):
    currentAuthor=single_author.objects.filter(uuid=userId).first()
    currentAuthorInbox = Inbox.objects.filter(author=currentAuthor).first()
    
    # inbox followers new post messages
    Inbox_new_post = currentAuthorInbox.items

    
    # my_posts_id_list = Post.objects.filter(author=currentAuthor).values_list('id')
    # likeds = Liked.objects.all()
    # likeds = Liked.objects.filter(type="liked")
    # for liked in likeds:
    #     for like in liked.items.all():
    #         if Post.objects.filter(id=like.object,author=currentAuthor).exists():
    #             postTitle = Post.objects.get(uuid = like.postId).title
    #             #print(like.summary)
    #             message = f"{like.author.username}{like.summary} | Post: {postTitle}"
    #             text.append(message)
    
    # inbox like messages
    text = []
    likeds = currentAuthorInbox.likes.all()
    for liked in likeds:
        likes = liked.items.all()
        for like in likes:
            text.append(like.summary)

    # inbox Comment messages
    comments = Comment.objects.all()
    comment_msg = []
    author_posts = Post.objects.filter(author=currentAuthor)
    for author_post in author_posts:
        if Comment.objects.filter(post=author_post).exists():
            for com in Comment.objects.filter(post=author_post):
                who_comment = com.author
                name = who_comment.display_name
                post_title = author_post.title
                comment_msg.append(name + " comments your post: " + post_title + ", with comment " + '"' + com.comment + '"' )
    
    # inbox Request messages
    re = currentAuthorInbox.followRequests.all()

    # accept the follow requests
    if request.method == 'POST' and 'delete' in request.POST:
        deleted_request_actor_id = request.POST['delete']
        deleted_request_actor = single_author.objects.get(id= deleted_request_actor_id)
        deleted_request_object = single_author.objects.get(uuid=userId)
        FollowRequest.objects.get(Q(actor = deleted_request_actor)&Q(object = deleted_request_object)).delete()

            
    return render(request, 'inbox/inbox.html',{
        "currentAuthorInbox": currentAuthorInbox,
        "userId": userId,
        "text": text,
        "Inbox_new_post": Inbox_new_post,
        "comment_msg": comment_msg,
        "requests": re,
    })

@login_required(login_url='/login/')
def search_result(request,userId,searched):
    if request.method == "POST":
        result = request.POST['searched']
        find_user = single_author.objects.filter(username = result)
        return render(request, 'search_result.html',{'userId':userId,
                                                    'searched':result, 
                                                    'searchResult':find_user})
    else:
        result = searched
        find_user = single_author.objects.filter(username = result)
        return render(request, 'search_result.html',{'userId':userId,'searched':result,'searchResult':find_user})





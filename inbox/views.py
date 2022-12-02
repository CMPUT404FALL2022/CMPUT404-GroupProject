from django.shortcuts import render
from authors.models import single_author
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from .models import InboxItem
from post.models import Liked, Like, Post
from .models import Inbox


@login_required(login_url='/login/')
def my_inbox(request,userId):
    currentAuthor=single_author.objects.filter(uuid=userId).first()
    currentAuthorInbox = Inbox.objects.filter(author=currentAuthor).first()
    Inbox_new_post = currentAuthorInbox.items
    #print(Inbox_new_post)

    # get data from liked model --- M
    my_posts_id_list = Post.objects.filter(author=currentAuthor).values_list('id')
    likeds = Liked.objects.all()
    text = []
    likeds = Liked.objects.filter(type="liked")
    for liked in likeds:
        for like in liked.items.all():
            if Post.objects.filter(id=like.object,author=currentAuthor).exists():
                #print(like.summary)
                message = like.summary + ", post id: " + like.object
                text.append(message)

    

    return render(request, 'inbox/inbox.html',{
        "currentAuthorInbox": currentAuthorInbox,
        "userId": userId,
        "text": text,
        "Inbox_new_post": Inbox_new_post
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

@login_required(login_url='/login/')
def author_inbox(request,userId):
    currentAuthor=single_author.objects.get(uuid=userId)
    
    if not Inbox.objects.filter(author=currentAuthor).exists():
        myInbox = Inbox.objects.create(author=currentAuthor,items=None)
        myInbox.save()
    
    all_author_posts = Post.objects.filter(uuid=userId)
    
    #currentAuthorInbox = Inbox.objects.get(author=currentAuthor)
    # bugs here
    currentAuthorInbox =  Inbox.objects.update(author=currentAuthor,items=all_author_posts)
    #currentAuthorInbox.save()
    # currentAuthorInbox = Inbox.objects.get(author=currentAuthor)
    # for post in currentAuthorInbox.items:
    #     postId = post.id
    #     all_likes_from_this_post = Like.objects.filter(object=postId)
    return render(request, 'inbox/inbox.html',{
        # "currentAuthorInbox": currentAuthorInbox,
        "userId": userId,
        # "all_likes_from_this_post": all_likes_from_this_post,
    })
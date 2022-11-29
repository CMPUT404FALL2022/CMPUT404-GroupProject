from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .post_forms import post_form, Comment_form
from .models import Post,Comment
from authors.models import single_author,Followers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models import Q
from inbox.models import InboxItem
import requests
from requests.auth import HTTPBasicAuth


# Create your views here.

@login_required(login_url='/login/')
def home_page(request,userId):
    booleanOfalert = False
    #这里要加判定
    # print(f"11111111111111111111{request.user}")
    # all_posts = Post.objects.all()
    all_posts = Post.objects.filter(unlisted=False, visibility="PUBLIC")
    post_comments_dict = {}
    
    #get comments
    for post in all_posts:
        oneListComment = Comment.objects.filter(post__uuid = post.uuid)

        post_comments_dict[post] = oneListComment
        
    if request.method == 'POST' and 'searched' in request.POST:
        searched = request.POST['searched']
        #two para in the followers model
        myself = single_author.objects.get(uuid=userId)
        followed = single_author.objects.filter(username=searched)
        #checkout if searched user exists
        if followed.count()!= 0:
            booleanOfalert == False
            #checkout if myself exists in the followers model
            exist_myself = Followers.objects.filter(Q(author__uuid=userId) & Q(follower__username=searched))
            #not exist in the followers model
            if exist_myself.count() == 0:
                # if myself["uuid"] != followed.uuid:
                my_follower = Followers()
                my_follower.author = single_author.objects.get(uuid=userId)
                my_follower.follower = single_author.objects.get(username=searched)
                my_follower.save()
            return HttpResponseRedirect(reverse("search-result",args=[userId,searched]))
        else:
            booleanOfalert == True

    others_posts = []
    others_posts_dict = {}
    #this is for others databases for group T05
    T05Url = "https://fallprojback.herokuapp.com/authors/ce20e705cbca4085955ff9f915854e43/posts/27f4ff47-6d30-4927-ae99-48323a228a0c"
    res = requests.get(T05Url)
    others_users = res.json()
    others_posts.append(others_users)

    T05Url2 = "https://fallprojback.herokuapp.com/authors/4843b801d83e4a5bb0b08f8716d3cba2/posts/018d6704-7f2b-49c2-b140-49a0394dd8ae"
    res = requests.get(T05Url2)
    others_users = res.json()
    others_posts.append(others_users)
    # T05Url = "https://fallprojback.herokuapp.com/authors/"
    # res = requests.get(T05Url)

    # others_users = res.json().get("items")
    # for user in others_users:
    #     postUrl = f"{user['id']}/posts"
    #     res = requests.get(postUrl)
    #     oneuser_post = res.json()
    #     print(f"BBBBBBBBBBBBBBBBBBBB{oneuser_post}")
    #     for post in oneuser_post:
    #         others_posts.append(post)

    
    #this is for others databases for group T16
    T16Url = "https://team-sixteen.herokuapp.com/posts/"
    res = requests.get(T16Url)
    print(res)
    T16_posts = res.json().get("items")
    
    for post in T16_posts:
        if len(post['content']) <= 200:
            others_posts.append(post)
            # res = requests.get(post['comments'])
            # others_comments = res.json().get("items")
            # others_posts_dict[post] = others_comments

            
    return render(request,"post/index.html",{
        "booleanOfalert":booleanOfalert,
        "post_comments_dict": post_comments_dict,
        "all_posts": all_posts,
        "others_posts": others_posts,
        # "others_posts_dict":others_posts_dict,
        "userId": userId,
    })
    
# def posts(request):
#     return render(request, 'post/post_in_div.html', {
#         'posts': Post.objects.all()
#     })

@login_required(login_url='/login/')
def create_post(request,userId):
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(newPost.uuid)}"
            newPost.source = newPost.id
            newPost.origin = newPost.id
            currentAuthor = single_author.objects.get(uuid = userId)
            newPost.author = currentAuthor
            # newPost.title = form.cleaned_data['title']
            # newPost.content = form.cleaned_data['content']
            # newPost.description = form.cleaned_data['description']
            # newPost = Post(title = form.cleaned_data['title'],description = form.cleaned_data['description'],content = form.cleaned_data['content'],Categories = form.cleaned_data['Categories'],visibility = form.cleaned_data['visibility'],textType = form.cleaned_data['textType'])

            newPost.save()
            print(f"This is hehahahahaa{newPost.__str__()}")
            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = post_form()
        return render(request,"post/create_new_post.html",{
            'form':form,
            'userId':userId
        })


@login_required(login_url='/login/')
def create_comment(request,userId,postId):
    if request.method == 'POST':
        form = Comment_form(request.POST)
        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(postId)}/comments/{str(newComment.uuid)}"
            currentAuthor = single_author.objects.get(uuid = userId)
            newComment.author = currentAuthor

            currentPost = Post.objects.get(uuid = postId)
            newComment.post = currentPost
            newComment.save()
            print(f"This is hehahahahaa{newComment.__str__()}")
            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = Comment_form()
        return render(request,"post/create_new_post.html",{
            'form':form,
            'userId':userId
        })


@login_required(login_url='/login/')
def create_like(request,userId,postId):
    item_type = "like"
    item_id = "1"
    item = postId
    currentAuthor = single_author.objects.get(uuid = userId)
    inboxitem = InboxItem.objects.create(item_type = item_type, item_id = item_id, item = item, author = currentAuthor)
    inboxitem.save()
    response = HttpResponse('Like created')
    response.status_code = 201
    return response
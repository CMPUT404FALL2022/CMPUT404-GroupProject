from django.shortcuts import render
# from SocialDistribution import post
from authors.models import single_author
from post.models import Post
from post.post_forms import post_form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from .forms import followRequestForm
from authors.models import Followers
from .forms import EditForm
from django.contrib.auth.decorators import login_required
import sqlite3
from django.db.models import Q
from authors.models import FollowRequest
# Create your views here.

# def my_page(request, userId):
#     return render(request,'me.html')

# def my_post_page(request, userId):
#     return render(request,'my_post.html')

@login_required(login_url='/login/')
def my_profile(request, userId):
    if request.method == 'POST' and 'delete' in request.POST:
        user_id = request.POST['delete']
        Followers.objects.get(Q(author__uuid = userId)&Q(follower__uuid = user_id)).delete()
        FollowRequest.objects.get(Q(actor__uuid = userId)&Q(object__uuid = user_id)).delete()
        return HttpResponseRedirect(reverse("profile-page",args=[userId]))
    

    
    all_posts = Post.objects.filter(author__uuid = userId)
    befriend_list = Followers.objects.filter(author__uuid = userId)
    
    true_friend_list = []
    true_friend_list_id_name = {}
    for befriend in befriend_list:
        # if befriend.follower.uuid != userId:
        who_followed_me = Followers.objects.filter(Q(author__uuid = befriend.follower.uuid)& Q(follower__uuid = userId))
        
        
        if who_followed_me.count() > 0:
            true_friend_list.append(who_followed_me)
    
    for friend in true_friend_list:
        
        true_friend_list_id_name[friend[0].author.uuid] = friend[0].author.username

    return render(request,'my_profile.html',{
        "all_posts": all_posts,
        "userId": userId,
        "befriend_list":befriend_list,
        "true_friend_list_id_name":true_friend_list_id_name
    })


@login_required(login_url='/login/')
def my_profile_modify(request, userId, postId):
    
    if request.method == 'POST' and 'mod' in request.POST:
        form = post_form(request.POST,request.FILES)
        if form.is_valid():
            
            newPost = Post.objects.get(uuid = postId)
            # form = form(newPost=newPost)

            newPost.title = form.cleaned_data['title']
            newPost.content = form.cleaned_data['content']
            newPost.textType = form.cleaned_data['textType']
            newPost.description = form.cleaned_data['description']
            newPost.Categories = form.cleaned_data['Categories']
            newPost.visibility = form.cleaned_data['visibility']
            newPost.post_image = form.cleaned_data['post_image']
            
            # newPost = Post(title = form.cleaned_data['title'],description = form.cleaned_data['description'],content = form.cleaned_data['content'],Categories = form.cleaned_data['Categories'],visibility = form.cleaned_data['visibility'],textType = form.cleaned_data['textType'])
            newPost.save()
    
            print(f"This is hehahahahaa{newPost.__str__()}")
            return HttpResponseRedirect(reverse("profile-page",args=[userId]))

    elif request.method == 'POST' and 'del' in request.POST:
        Post.objects.get(uuid = postId).delete()
        return HttpResponseRedirect(reverse("profile-page",args=[userId]))
    else:
        form = post_form()
        return render(request,"me_profile_modify.html",{
            'form':form,
            'userId':userId
    })

@login_required(login_url='/login/')
def myinfo(request, userId):
    all_info = single_author.objects.get(uuid = userId)
    return render(request, 'myinfo.html',{
        "all_info": all_info,
        "userId": userId
    })

@login_required(login_url='/login/')
def myinfoedit(request, userId):
    author = single_author.objects.get(uuid = userId)
    form = EditForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
    return render(request, 'editmyinfo.html',{
        "all_info": author,
        "userId": userId,
        "form": form
    })


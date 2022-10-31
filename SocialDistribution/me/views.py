from django.shortcuts import render
# from SocialDistribution import post
from authors.models import single_author
from post.models import Post
from post.post_forms import post_form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import followRequestForm
from authors.models import Followers
from .forms import EditForm
import sqlite3
# Create your views here.

# def my_page(request, userId):
#     return render(request,'me.html')

# def my_post_page(request, userId):
#     return render(request,'my_post.html')

def my_profile(request, userId):
    all_posts = Post.objects.filter(author__id = userId)
    if request.method == "POST":
        # currentUser = request.user
        # form = followRequestForm(request.POST)
        # receiver = single_author.objects.filter(username = form.cleaned_data['object'])
        # currentAuthor = single_author.objects.filter(username = currentUser)
         
        # if form.is_valid():
        #     if receiver.exists():
        #         getFollowerList = Followers.objects.get(author = receiver)
        #         getFollowerList.items.add(newFollower)
        #         getFollowerList.save()
        pass
    else:
        requestForm = followRequestForm()

    return render(request,'my_profile.html',{
        "all_posts": all_posts,
        "userId": userId
    })



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
def myinfo(request, userId):
    all_info = single_author.objects.get(id = userId)
    return render(request, 'myinfo.html',{
        "all_info": all_info,
        "userId": userId
    })

def myinfoedit(request, userId):
    all_info = single_author.objects.get(id = userId)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            # conflict with login
            #password = form.cleaned_data['password']
            display_name = form.cleaned_data['display_name']
            github = form.cleaned_data['github']
            
            #--------------sql query to update the database----------------
            conn = sqlite3.connect('./db.sqlite3')
            c = conn.cursor()
            #c.execute('UPDATE authors_single_author SET password = ?, display_name = ? , github = ? WHERE id = ?;',(password,display_name,github,userId))
            c.execute('UPDATE authors_single_author SET display_name = ? , github = ? WHERE id = ?;',(display_name,github,userId))
            conn.commit()
            conn.close()
    form = EditForm()
    return render(request, 'editmyinfo.html',{
        "all_info": all_info,
        "userId": userId,
        "form": form

    })

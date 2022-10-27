from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .post_forms import post_form, Comment_form
from .models import Post
from authors.models import single_author
from django.urls import reverse
import uuid

# Create your views here.

def home_page(request,userId):
    #这里要加判定
    print(f"11111111111111111111{request.user}")
    all_posts = Post.objects.all()
    # all_posts = Posts.object.get(visibility = 'public')

    return render(request,"post/index.html",{
        "all_posts": all_posts,
        "userId": userId
    })
    
# def posts(request):
#     return render(request, 'post/post_in_div.html', {
#         'posts': Post.objects.all()
#     })

def create_post(request,userId):
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.id = f"{request.build_absolute_uri('/')}authors/{str(userId)}/posts/{str(newPost.uuid)}"
            newPost.source = newPost.id
            newPost.origin = newPost.id
            currentAuthor = single_author.objects.get(id = userId)
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
            'form':form
            
        })



def create_comment(request,userId):
    if request.method == 'POST':
        form = Comment_form(request.POST)
        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.id = f"{request.build_absolute_uri('/')}authors/{str(userId)}/posts/{str(newComment.uuid)}"
            currentAuthor = single_author.objects.get(id = userId)
            newComment.author = currentAuthor

            
            newComment.save()
            print(f"This is hehahahahaa{newComment.__str__()}")
            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = Comment_form()
        return render(request,"post/create_new_post.html",{
            'form':form
            
        })
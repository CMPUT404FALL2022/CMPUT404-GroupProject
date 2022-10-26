from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .post_forms import post_form
from .models import Post
from authors.models import single_author
from django.urls import reverse
import uuid

# Create your views here.

def home_page(request,userId):
    print(userId)
    return render(request,"post/index.html")

# def posts(request):
#     return render(request, 'post/post_in_div.html', {
#         'posts': Post.objects.all()
#     })

def create_post(request):
    if request.method == 'POST':
        form = post_form(request.POST)
        if form.is_valid():
            new_post = Post(title = form.cleaned_data['title'],description = form.cleaned_data['description'],content = form.cleaned_data['content'],Categories = form.cleaned_data['Categories'])
            new_post.save()
    
            return HttpResponseRedirect(reverse("create-page"))


    else:
        form = post_form()
        return render(request,"post/create_new_post.html",{
            'form':form
            
        })

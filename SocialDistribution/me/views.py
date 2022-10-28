from django.shortcuts import render
# from SocialDistribution import post
from authors.models import single_author
from post.models import Post
from post.post_forms import post_form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# def my_page(request, userId):
#     return render(request,'me.html')

# def my_post_page(request, userId):
#     return render(request,'my_post.html')

def my_profile(request, userId):
    all_posts = Post.objects.all()

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
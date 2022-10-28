from django.shortcuts import render
from authors.models import single_author
from post.models import Post
from .forms import EditForm
import sqlite3
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
            password = form.cleaned_data['password']
            display_name = form.cleaned_data['display_name']
            github = form.cleaned_data['github']
            
            #--------------sql query to update the database----------------
            conn = sqlite3.connect('./db.sqlite3')
            c = conn.cursor()
            c.execute('UPDATE authors_single_author SET password = ?, display_name = ? , github = ? WHERE id = ?;',(password,display_name,github,userId))
            conn.commit()
            conn.close()
    form = EditForm()
    return render(request, 'editmyinfo.html',{
        "all_info": all_info,
        "userId": userId,
        "form": form

    })

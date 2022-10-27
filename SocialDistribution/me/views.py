from django.shortcuts import render
from authors.models import single_author

# Create your views here.

def my_page(request, userId):
    current_user = single_author.objects.get(id = userId)
    return render(request,'me.html')

def my_post_page(request, userId):
    return render(request,'my_post.html')
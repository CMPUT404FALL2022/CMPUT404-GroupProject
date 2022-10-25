from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request,"post/index.html")

def posts(request):
    pass

def create_post(request):
    return render(request, "post/create_new_post.html")
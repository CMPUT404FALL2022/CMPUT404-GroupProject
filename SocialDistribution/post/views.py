from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request,"post/index.html")

def posts(request):
    pass

def post_detail(request):
    pass
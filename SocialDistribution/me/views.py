from django.shortcuts import render
from authors.models import single_author

# Create your views here.

def my_page(request, userId):
    return render(request,'me.html')

<<<<<<< Updated upstream
def my_post_page(request, userId):
    return render(request,'my_post.html')
=======
    return render(request,'my_profile.html',{
        "all_posts": all_posts,
        "userId": userId
    })


def myinfo(request, userId):
    all_info = single_author.objects.get()
    return render(request, 'myinfo.html',{
        "all_info": all_info,
        "userId": userId

    })
>>>>>>> Stashed changes

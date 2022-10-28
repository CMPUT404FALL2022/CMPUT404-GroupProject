from django.shortcuts import render
from authors.models import single_author

from django.http import HttpResponse

def my_inbox(request,userId):

    return render(request, 'inbox.html',{
       
        "userId": userId
    })
    #return HttpResponse("You're looking at question.")

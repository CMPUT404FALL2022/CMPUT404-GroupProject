from django.shortcuts import render
from django.contrib import messages
from authors.models import single_author
from .models import Followers,single_author
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


@login_required(login_url='/login/')
def search(request,userId):
    if request.method == 'POST':
        searched = request.POST['searched']
        myself = single_author.objects.get(id=userId)
        followed = single_author.objects.filter(display_name=searched)
        print(searched)
        # if followed.count() == 0:
        #     messages.error(request,"No This User")
        #     return HttpResponseRedirect(reverse("home-page",args=[userId]))
    return HttpResponseRedirect(reverse("home-page",args=[userId]))
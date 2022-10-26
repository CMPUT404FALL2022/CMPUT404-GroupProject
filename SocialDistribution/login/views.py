
import argparse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import single_author
from authors.models import authors
from django.shortcuts import redirect
from django.urls import reverse
from .forms import SignUpForm
from .forms import LoginForm

import uuid
# Create your views here.
def log_in(request):
    #login by username and password
    isNotPasswordMatch = False
    isNotUsernameExist = False

    if request.method == 'POST':
        username = request.POST.get('username')
        
        if single_author.objects.filter(username=username).exists():
            password = request.POST.get('password')
            storedUser = single_author.objects.get(username=username)
            storedUserPassword = storedUser.password
            userId = storedUser.id
            if storedUserPassword == password:
                #redirect this for now
                # return HttpResponseRedirect("post/index.html",{
                #     'username':storedUser
                # })
                # return HttpResponseRedirect("")
                return HttpResponseRedirect(reverse("home-page",args=[userId]))
            else:
                form = LoginForm()
                isNotPasswordMatch = True
                return render(request, 'login/login.html',{
                    "form":form,
                    'isNotPasswordMatch':isNotPasswordMatch
                })
        else:
            form = LoginForm()
            isNotUsernameExist = True
            return render(request, 'login/login.html',{
                "form":form,
                'isNotUsernameExist':isNotUsernameExist
            })
    else:
        form = LoginForm()

    return render(request,"login/login.html",{
        "form":form,
        "isNotUsernameExist":isNotUsernameExist,
        "isNotPasswordMatch":isNotPasswordMatch
    })

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            authorHost = request.META.get('HTTP_HOST')
            authorId = str(uuid.uuid4())
            
            authorUrl = 'http://'+authorHost+'/authors/'+authorId
        
            new_author = single_author(username = form.cleaned_data['username'],
                                        password = form.cleaned_data['password'],
                                        id = authorId,
                                        host = authorHost,
                                        display_name=form.cleaned_data['display_name'],
                                        url = authorUrl)
            new_author.save()
            return HttpResponseRedirect('/login')
    else:
        form = SignUpForm()

    return render(request,"login/signup.html",{
        'form':form
    })






from urllib.robotparser import RequestRate
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import single_author
from .forms import SignUpForm

import uuid

# Create your views here.
def log_in(request):
    return render(request,"login/login.html")

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






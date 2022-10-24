from urllib.robotparser import RequestRate
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authors.models import single_author
from django.shortcuts import redirect
from .forms import SignUpForm

# Create your views here.
def log_in(request):
    return render(request,"login/login.html")

def sign_up(request):
    # submittted = False
    
    # if request.method == "post":
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    # else:
    #     form = SignUpForm()
    #     if 'submittted' in request.GET:
    #         submittted = True

    #if is a POST request
    if request.method == "POST":
        entered_username = request.POST['username']
        entered_password = request.POST['password']

        #check if entered_username and entered_password are null
        if entered_username == '' or entered_password == '':
            return render(request,"login/signup.html",{
                'has_error': True
            })
        print({'username':entered_username,'password':entered_password})
        #HTTPResponseRedirect back to log in page
        
        return HttpResponseRedirect('/login')

    
    return render(request,"login/signup.html")

@api_view(['POST'])
def create_new_user(request):
    #Create a new object from single_author
    pass





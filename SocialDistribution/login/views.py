from django.shortcuts import render

# Create your views here.
def log_in(request):
    return render(request,"login/login.html")

def sign_up(request):
    return render(request,"login/signup.html")
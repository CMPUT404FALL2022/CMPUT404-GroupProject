from django.shortcuts import render

#from django.http import HttpResponse

def create(request):
    return render(request,'indox.html')
    #return HttpResponse("You're looking at question.")

from django.shortcuts import render
from authors.models import single_author
from .models import InboxItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='/login/')
def my_inbox(request,userId):
    currentAuthor=single_author.objects.filter(id=userId).first()
    currentAuthorInbox = InboxItem.objects.filter(author__id=currentAuthor.id)

    return render(request, 'inbox/inbox.html',{
        "currentAuthorInbox": currentAuthorInbox,
        "userId": userId
    })


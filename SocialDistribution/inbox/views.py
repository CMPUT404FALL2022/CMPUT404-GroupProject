from django.shortcuts import render
from authors.models import single_author
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import InboxItem


@login_required(login_url='/login/')
def my_inbox(request,userId):
    currentAuthor=single_author.objects.filter(uuid=userId).first()
    currentAuthorInbox = InboxItem.objects.filter(author__uuid=currentAuthor.uuid)
    return render(request, 'inbox/inbox.html',{
        "currentAuthorInbox": currentAuthorInbox,
        "userId": userId
    })


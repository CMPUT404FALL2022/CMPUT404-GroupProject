from django.shortcuts import render
# from SocialDistribution import post
from authors.models import single_author,ExternalFollowers
from post.models import Post, Node
from post.post_forms import post_form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from .forms import followRequestForm
from authors.models import Followers
from .forms import EditForm
from django.contrib.auth.decorators import login_required
import sqlite3
from django.db.models import Q
from requests.auth import HTTPBasicAuth
import requests
from authors.models import FollowRequest
# Create your views here.

# def my_page(request, userId):
#     return render(request,'me.html')

# def my_post_page(request, userId):
#     return render(request,'my_post.html')

@login_required(login_url='/login/')
def my_profile(request, userId):
    if request.method == 'POST' and 'delete' in request.POST:
        user_id = request.POST['delete']
        Followers.objects.get(Q(author__uuid = userId)&Q(follower__uuid = user_id)).delete()
        deleted_request_actor = single_author.objects.get(uuid=userId)
        deleted_request_object = single_author.objects.get(uuid=user_id)
        FollowRequest.objects.get(Q(actor = deleted_request_actor)&Q(object = deleted_request_object)).delete()
        return HttpResponseRedirect(reverse("profile-page",args=[userId]))
    

    
    all_posts = Post.objects.filter(author__uuid = userId)
    befriend_list = Followers.objects.filter(author__uuid = userId)
    ExternalFriendList = ExternalFollowers.objects.filter(author__uuid = userId)
    true_friend_list = []
    true_friend_list_id_name = {}
    for befriend in befriend_list:
        # if befriend.follower.uuid != userId:
        who_followed_me = Followers.objects.filter(Q(author__uuid = befriend.follower.uuid)& Q(follower__uuid = userId))
        
        
        if who_followed_me.count() > 0:
            true_friend_list.append(who_followed_me)
    
    for friend in true_friend_list:
        
        true_friend_list_id_name[friend[0].author.uuid] = friend[0].author.username
    


    if request.method == 'POST' and 'search-external' in request.POST:
        
        searchedFor = request.POST['search-external']
        searchedGroup = request.POST.get('group')
        node = Node.objects.filter(name = searchedGroup).first()
        if searchedGroup == '11':
            TeamUrl = f"{node.host}"
            res = requests.get(TeamUrl, auth = HTTPBasicAuth('11fifteen', '11fifteen'))
            teamAuthors = res.json().get("results")
            for author in teamAuthors:
                if author['displayName'] == searchedFor:
                    #在这里发好友邀请到inbox
                    me = single_author.objects.filter(uuid = userId).first()
                    #create a new external follower for this user
                    #if not exists
                    if len(ExternalFollowers.objects.filter(external_username = author['displayName'])) == 0:
                        newExternalAuthor = ExternalFollowers.objects.create(author = me,external_username = author['displayName'], external_id = author['id'], groupNumber = 11)
                        newExternalAuthor.save()
                    break




        elif searchedGroup == '16':
            TeamUrl = f"{node.host}authors"
            print(TeamUrl)
            res = requests.get(TeamUrl)
            teamAuthors = res.json().get("items")
            for author in teamAuthors:
                if author['displayName'] == searchedFor:
                    #在这里发好友邀请到inbox
                    me = single_author.objects.filter(uuid = userId).first()
                    #create a new external follower for this user
                    #if not exists
                    if len(ExternalFollowers.objects.filter(external_username = author['displayName'])) == 0:
                        newExternalAuthor = ExternalFollowers.objects.create(author = me,external_username = author['displayName'], external_id = author['id'], groupNumber = 16)
                        newExternalAuthor.save()
                    break




        elif searchedGroup == '18':
            TeamUrl = f"{node.host}"
            print(TeamUrl)


    return render(request,'my_profile.html',{
        "all_posts": all_posts,
        "userId": userId,
        "befriend_list":befriend_list,
        "true_friend_list_id_name":true_friend_list_id_name,
        "ExternalFriendList" : ExternalFriendList
    })


@login_required(login_url='/login/')
def my_profile_modify(request, userId, postId):
    
    if request.method == 'POST' and 'mod' in request.POST:
        form = post_form(request.POST,request.FILES)
        if form.is_valid():
            
            newPost = Post.objects.get(uuid = postId)
            # form = form(newPost=newPost)

            newPost.title = form.cleaned_data['title']
            newPost.content = form.cleaned_data['content']
            newPost.textType = form.cleaned_data['textType']
            newPost.description = form.cleaned_data['description']
            newPost.Categories = form.cleaned_data['Categories']
            newPost.visibility = form.cleaned_data['visibility']
            newPost.post_image = form.cleaned_data['post_image']
            
            # newPost = Post(title = form.cleaned_data['title'],description = form.cleaned_data['description'],content = form.cleaned_data['content'],Categories = form.cleaned_data['Categories'],visibility = form.cleaned_data['visibility'],textType = form.cleaned_data['textType'])
            newPost.save()
    
            print(f"This is hehahahahaa{newPost.__str__()}")
            return HttpResponseRedirect(reverse("profile-page",args=[userId]))

    elif request.method == 'POST' and 'del' in request.POST:
        Post.objects.get(uuid = postId).delete()
        return HttpResponseRedirect(reverse("profile-page",args=[userId]))
    else:
        form = post_form()
        return render(request,"me_profile_modify.html",{
            'form':form,
            'userId':userId
    })

@login_required(login_url='/login/')
def myinfo(request, userId):
    all_info = single_author.objects.get(uuid = userId)
    return render(request, 'myinfo.html',{
        "all_info": all_info,
        "userId": userId
    })

@login_required(login_url='/login/')
def myinfoedit(request, userId):
    # all_info = single_author.objects.get(uuid = userId)
#     if request.method == "POST":
#         form = EditForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('')
#             # conflict with login
#             #password = form.cleaned_data['password']
#             #display_name = form.cleaned_data['display_name']
#             #github = form.cleaned_data['github']
            
# #             #--------------sql query to update the database----------------
#     #         conn = sqlite3.connect('./db.sqlite3')
#     #         c = conn.cursor()
#     #         #c.execute('UPDATE authors_single_author SET password = ?, display_name = ? , github = ? WHERE id = ?;',(password,display_name,github,userId))
#     #         c.execute('UPDATE authors_single_author SET display_name = ? , github = ? WHERE id = ?;',(display_name,github,userId))
#     #         conn.commit()
#     #         conn.close()
#     form = EditForm()
#     return render(request, 'editmyinfo.html',{
#         "all_info": all_info,
#         "userId": userId,
#         "form": form

#     })
    author = single_author.objects.get(uuid = userId)
    form = EditForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
    return render(request, 'editmyinfo.html',{
        "all_info": author,
        "userId": userId,
        "form": form
    })


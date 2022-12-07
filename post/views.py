from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .post_forms import post_form, Comment_form, ExternalForm, UserSelectionForm
from .models import Post,Comment,Like,Liked,Node
from authors.models import single_author,Followers,ExternalFollowers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models import Q
#from inbox.models import InboxItem
from inbox.models import Inbox
import requests
from requests.auth import HTTPBasicAuth
from authors.models import FollowRequest
import json


# Create your views here.

@login_required(login_url='/login/')
def home_page(request,userId):
    booleanOfalert = False
    #这里要加判定
    # print(f"11111111111111111111{request.user}")
    # all_posts = Post.objects.all()
    all_posts = Post.objects.filter(unlisted=False, visibility="PUBLIC")
    post_comments_dict = {}
    userSelectionForm = UserSelectionForm(userId=userId)
    
    #get comments
    for post in all_posts:
        oneListComment = Comment.objects.filter(post__uuid = post.uuid)
        post_comments_dict[post] = oneListComment
        
    if request.method == 'POST' and 'searched' in request.POST:
        searched = request.POST['searched']
        #two para in the followers model
        myself = single_author.objects.get(uuid=userId)
        followed = single_author.objects.filter(username=searched)
        #checkout if searched user exists
        if followed.count()!= 0:
            booleanOfalert == False
            #checkout if myself exists in the followers model
            exist_myself = Followers.objects.filter(Q(author__uuid=userId) & Q(follower__username=searched))
            #not exist in the followers model
            if exist_myself.count() == 0:
                # if myself["uuid"] != followed.uuid:
                my_follower = Followers()
                my_follower.author = single_author.objects.get(uuid=userId)
                my_follower.follower = single_author.objects.get(username=searched)
                my_follower.save()

                # create friend request
                if not FollowRequest.objects.filter(actor=my_follower.author,object=my_follower.follower).exists():
                    actor_name = my_follower.author.display_name
                    #object_name = my_follower.follower.display_name
                    summary = actor_name + " wants to follow you!"
                    re = FollowRequest.objects.create(summary=summary,actor=my_follower.author,object=my_follower.follower)
                    
                    # request added to inbox
                    object_inbox = Inbox.objects.get(author=my_follower.follower)
                    object_inbox.followRequests.add(re)



            return HttpResponseRedirect(reverse("search-result",args=[userId,searched]))
        else:
            booleanOfalert == True

        
    currentAuthor = single_author.objects.filter(uuid=userId)     
    return render(request,"post/index.html",{
        "booleanOfalert":booleanOfalert,
        "post_comments_dict": post_comments_dict,
        "all_posts": all_posts,
        "userId": userId,
        "userSelectionForm":userSelectionForm,
    })
    
# def posts(request):
#     return render(request, 'post/post_in_div.html', {
#         'posts': Post.objects.all()
#     })

@login_required(login_url='/login/')
def create_post(request,userId):
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
        userSelectionForm = UserSelectionForm(userId = userId)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(newPost.uuid)}"
            newPost.source = newPost.id
            newPost.origin = newPost.id
            currentAuthor = single_author.objects.get(uuid = userId)
            newPost.author = currentAuthor
            # newPost.title = form.cleaned_data['title']
            # newPost.content = form.cleaned_data['content']
            # newPost.description = form.cleaned_data['description']
            # newPost = Post(title = form.cleaned_data['title'],description = form.cleaned_data['description'],content = form.cleaned_data['content'],Categories = form.cleaned_data['Categories'],visibility = form.cleaned_data['visibility'],textType = form.cleaned_data['textType'])
            newPost.save()
            #print(f"This is hehahahahaa{newPost.__str__()}")

            #send to a specific friend
            if newPost.visibility == 'FRIENDS':
                sendTo = request.POST.get('Send_To')
                print(sendTo)
                
                inbox = Inbox.objects.get(author__username = sendTo)

                inbox.items.add(newPost)

            # I tell all my followers that I have a new post
            current_author_followers = Followers.objects.filter(follower=currentAuthor)
            #print(current_author_followers)
            if current_author_followers.count() != 0:
                for item in current_author_followers:
                    
                    # new post added to inbox
                    follower = item.author
                    follower_inbox = Inbox.objects.get(author=follower)
                    follower_inbox.items.add(newPost)

            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = post_form()
        userSelectionForm = UserSelectionForm(userId = userId)
        return render(request,"post/create_new_post.html",{
            'form':form,
            'userId':userId,
            'userSelectionForm':userSelectionForm,
        })


@login_required(login_url='/login/')
def create_comment(request,userId,postId):
    if request.method == 'POST':
        form = Comment_form(request.POST)
        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(postId)}/comments/{str(newComment.uuid)}"
            currentAuthor = single_author.objects.get(uuid = userId)
            newComment.author = currentAuthor

            currentPost = Post.objects.get(uuid = postId)
            newComment.post = currentPost
            newComment.save()
            print(f"This is hehahahahaa{newComment.__str__()}")


            # comment added to inbox
            post_author = Post.objects.get(uuid=postId).author
            post_author_inbox = Inbox.objects.get(author=post_author)
            post_author_inbox.comments.add(newComment)

            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = Comment_form()
        return render(request,"post/create_new_post.html",{
            'form':form,
            'userId':userId
        })

@login_required(login_url='/login/')
def create_like(request,userId,postId):
    po = Post.objects.get(uuid = postId).id
    po_uuid = Post.objects.get(uuid = postId).uuid
    currentAuthor = single_author.objects.get(uuid = userId)
    author_name = currentAuthor.display_name
    summary = author_name + " Likes your post"
    if not Like.objects.filter(author=currentAuthor, summary=summary, object=po, postId = po_uuid).exists():
        like = Like.objects.create(author=currentAuthor, summary=summary, object=po, postId = po_uuid)
        like.save()
        if not Liked.objects.filter(postId=po).exists():
            print("fffffffffffffffffff")
            receiver_liked = Liked.objects.create(postId=po)       
        receiver_liked = Liked.objects.get(postId=po)
        receiver_liked.items.add(like)

        # Liked added to inbox
        post_author = Post.objects.get(uuid=postId).author
        post_author_inbox = Inbox.objects.get(author=post_author)
        post_author_inbox.likes.add(receiver_liked)

    # count like might be done in part 3
    #like_count = Like.objects.filter(object=object).count()
    return HttpResponseRedirect(reverse("home-page",args=[userId]))


def share_post(request,userId,postId):
    
    currentAuthor = single_author.objects.filter(uuid = userId).first()
    selectedPost = Post.objects.get(uuid=postId)
    
    if request.method == 'POST':
        sendTo = request.POST.get('Send_To')
        
        inbox = Inbox.objects.get(author__username = sendTo)

        inbox.items.add(selectedPost)


        return HttpResponseRedirect(reverse("home-page",args=[userId]))


    # my own post cannot shared by myself, but can share same post many times *
    # if old_post.author.uuid != currentAuthor.uuid:
    #     new_title = old_post.title
    #     new_postId = uuid.uuid4()
    #     new_id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(new_postId)}"
    #     new_source = id
    #     new_origin = id
    #     new_description = old_post.description
    #     new_content_type = old_post.contentType
    #     new_content = old_post.content
        
    #     new_author = currentAuthor
    #     new_categories = old_post.Categories
    #     new_count = 0
    #     new_visibility = old_post.visibility
    #     new_unlisted = old_post.unlisted
    #     new_textType = old_post.textType
    #     new_post_image = old_post.post_image
    #     shared_post = Post.objects.create(title=new_title, uuid=new_postId, id=new_id, source=new_source, origin=new_origin,
    #                                     description=new_description, contentType=new_content_type,
    #                                     content=new_content, author=new_author, Categories=new_categories,
    #                                     count=new_count, visibility=new_visibility, unlisted=new_unlisted,
    #                                     textType=new_textType, post_image=new_post_image)
    #     shared_post.save() 
    
    else:
        userSelectionForm = UserSelectionForm(userId = userId)
        return render(request,"post/share_posts.html",{
                'userSelectionForm':userSelectionForm,
                'userId':userId,
                'post':selectedPost,
            })



@login_required(login_url='/login/')
def get_node(request,userId):
    if request.method == 'POST':
        currentAuthor = single_author.objects.filter(uuid = userId).first()
        form = post_form(request.POST,request.FILES)
        groupNumber = ExternalFollowers.objects.filter(external_id = form.data['friend']).first().groupNumber

        if groupNumber == 5:
            Url = f"{form.data['friend']}/posts/"
            print(Url)
            jsonFile = {
                "type": "post",
                "title": f"{form.data['title']}",
                "origin": f"{form.data['friend']}",
                "description": f"{form.data['description']}",
                "contentType": f"{form.data['contentType']}",
                "content": f"{form.data['content']}",
                "author": f"{form.data['friend']}",
                "count": 0,
                "visibility": "PUBLIC"
            }
            
            x = requests.post(Url, data = jsonFile, auth = HTTPBasicAuth('admin', 'admin'))

        elif groupNumber == 16:
            pass

        elif groupNumber == 11:
            pass

        return HttpResponseRedirect(reverse("home-page",args=[userId]))
    else:
        
        form = ExternalForm(userId = userId)
        all_nodes = Node.objects.all()
        all_posts = []

        for node in all_nodes:
            if node.name == 16:
                TeamUrl = f"{node.host}{node.api}"
                
                res = requests.get(TeamUrl)
                teamPosts = res.json().get("items")
                
                for post in teamPosts:
                    if len(post['content']) <= 200:
                        image_url = f"{post['id']}/image"
                        res = requests.get(image_url)
                        if res.status_code == 200:
                            post['image'] = image_url
                        else:
                            post['image'] = None
                        comment_url = post['comments']
                        res = requests.get(comment_url)
                        comments = res.json().get("items")
                        post['comment'] = comments
                        all_posts.append(post)
                    
            elif node.name == 5:
                TeamUrl = f"{node.host}{node.api}/posts_all"
                res = requests.get(TeamUrl, auth = HTTPBasicAuth('admin', 'admin'))
                teamPosts = res.json().get("items")
                for post in teamPosts:
                    substr = "localhost"
                
                    if substr not in f"{post['id']}":
                        try:
                            image_url = f"{post['id']}/image"
                            res = requests.get(image_url)
                        except:
                            pass

                        if res.status_code == 200:
                            post['image'] = image_url
                        else:
                            post['image'] = None
                        comment_url = post['comments']
                        try:
                            res = requests.get(comment_url)
                        except:
                            pass
                        if res.status_code == 200:
                            comments = res.json().get("comments")
                            post['comment'] = comments
                        all_posts.append(post)
                        # if res.status_code == 200:
                        #     teamPosts = res.json()
                        #     print(teamPosts)

            elif node.name == 11:
                TeamUrl = f"{node.host}{node.api}"
                res = requests.get(TeamUrl, auth = HTTPBasicAuth('11fifteen', '11fifteen'))
                teamPosts = res.json().get("results")
                
                for post in teamPosts:
                    if len(post['content']) <= 200:
                        image_url = f"{post['id']}/image"
                        res = requests.get(image_url)
                        if res.status_code == 200:
                            post['image'] = image_url
                        else:
                            post['image'] = None
                        comment_url = post['comments']
                        res = requests.get(comment_url)
                        if res.status_code == 200:
                            comments = res.json().get("items")
                            post['comment'] = comments
                        all_posts.append(post)




            # elif node.name == 18:
                # TeamUrl = f"{node.host}{node.api}"
                # res = requests.get(TeamUrl, auth = HTTPBasicAuth('t18user1', 'Password123!'))
                # teamPosts = res.json().get("items")
                # for post in teamPosts:
                #     if len(post['content']) <= 200:
                #         # image_url = f"{post['id']}/image"
                #         # res = requests.get(image_url)
                #         # if res.status_code == 200:
                #         #     post['image'] = image_url
                #         # else:
                #         post['image'] = None
                #         comment_url = post['comments']
                #         res = requests.get(comment_url)
                #         if res.status_code == 200:
                #             comments = res.json().get("items")
                #             post['comment'] = comments
                #         all_posts.append(post)
            


        return render(request,"post/node.html",{
            'userId':userId,
            'all_posts':all_posts,
            'ExternalForm':form,
        })
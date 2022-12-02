from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .post_forms import post_form, Comment_form
from .models import Post,Comment,Like,Liked
from authors.models import single_author,Followers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models import Q
#from inbox.models import InboxItem
from inbox.models import Inbox




# Create your views here.

@login_required(login_url='/login/')
def home_page(request,userId):
    booleanOfalert = False
    #这里要加判定
    # print(f"11111111111111111111{request.user}")
    # all_posts = Post.objects.all()
    all_posts = Post.objects.filter(unlisted=False, visibility="PUBLIC")
    post_comments_dict = {}
    
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
            return HttpResponseRedirect(reverse("search-result",args=[userId,searched]))
        else:
            booleanOfalert == True

        
    currentAuthor = single_author.objects.filter(uuid=userId)     
    return render(request,"post/index.html",{
        "booleanOfalert":booleanOfalert,
        "post_comments_dict": post_comments_dict,
        "all_posts": all_posts,
        "userId": userId,
    })
    
# def posts(request):
#     return render(request, 'post/post_in_div.html', {
#         'posts': Post.objects.all()
#     })

@login_required(login_url='/login/')
def create_post(request,userId):
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
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

            # I tell all my followers that I have a new post
            current_author_followers = Followers.objects.filter(follower=currentAuthor)
            #print(current_author_followers)
            if current_author_followers.count() != 0:
                for item in current_author_followers:
                    follower = item.author
                    follower_inbox = Inbox.objects.get(author=follower)

                    follower_inbox.items.add(newPost)

            return HttpResponseRedirect(reverse("home-page",args=[userId]))


    else:
        form = post_form()
        return render(request,"post/create_new_post.html",{
            'form':form,
            'userId':userId
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
    # item_type = "like"
    # item_id = "1"
    # item = postId
    currentAuthor = single_author.objects.get(uuid = userId)
    author_name = currentAuthor.display_name
    summary = author_name + " Likes your post"
    #inboxitem = InboxItem.objects.create(item_type = item_type, item_id = item_id, item = item, author = currentAuthor)
    #inboxitem.save()
    if not Like.objects.filter(author=currentAuthor, summary=summary, object=po, postId = po_uuid).exists():
        like = Like.objects.create(author=currentAuthor, summary=summary, object=po, postId = po_uuid)
        like.save()
        if not Liked.objects.filter(postId=po).exists():
            print("fffffffffffffffffff")
            receiver_liked = Liked.objects.create(postId=po)       
        receiver_liked = Liked.objects.get(postId=po)
        receiver_liked.items.add(like)
    # count like might be done in part 3
    #like_count = Like.objects.filter(object=object).count()
    #response = HttpResponse('Like created')
    #response.status_code = 201
    return HttpResponseRedirect(reverse("home-page",args=[userId]))


def share_post(request,userId,postId):
    old_post = Post.objects.filter(uuid=postId).first()
    currentAuthor = single_author.objects.filter(uuid = userId).first()
    # my own post cannot shared by myself, but can share same post many times *
    if old_post.author.uuid != currentAuthor.uuid:
        new_title = old_post.title
        new_postId = uuid.uuid4()
        new_id = f"{request.build_absolute_uri('/')}service/authors/{str(userId)}/posts/{str(new_postId)}"
        new_source = id
        new_origin = id
        new_description = old_post.description
        new_content_type = old_post.contentType
        new_content = old_post.content
        
        new_author = currentAuthor
        new_categories = old_post.Categories
        new_count = 0
        new_visibility = old_post.visibility
        new_unlisted = old_post.unlisted
        new_textType = old_post.textType
        new_post_image = old_post.post_image
        shared_post = Post.objects.create(title=new_title, uuid=new_postId, id=new_id, source=new_source, origin=new_origin,
                                        description=new_description, contentType=new_content_type,
                                        content=new_content, author=new_author, Categories=new_categories,
                                        count=new_count, visibility=new_visibility, unlisted=new_unlisted,
                                        textType=new_textType, post_image=new_post_image)
        shared_post.save()   
    # old_post.pk = None
    # shared_post = old_post
    # print(type(shared_post))
    #shared_post = Post.objects.update(id=new_id, source=new_source,origin=new_origin,author=new_author,count=new_count)
    # print(type(shared_post))
    # shared_post.save()
    # old_post = Post.objects.update(id=id, source=source,origin=origin,author=author)
    # old_post.save()
    return HttpResponseRedirect(reverse("home-page",args=[userId]))


@login_required(login_url='/login/')
def get_node(request,userId):
    




    return render(request,"post/node.html",{
            'userId':userId
        })
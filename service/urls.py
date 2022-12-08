from django.urls import path
from . import views


urlpatterns = [
    # path("", views.authors, name="authors"),
    path('posts/',views.getAllPublicPosts,name="all-posts-list"),
    path('authors/',views.authorsList, name="authors-list"),
    path('authors/<str:pk>/',views.singleAuthor,name="singleAuthor"),
    path('authors/<str:pk>/posts/',views.Posts,name="onesPosts"),
    path('authors/<str:pk>/posts/<str:postsId>/',views.getPost,name="getPosts"),
    path('authors/<str:pk>/posts/<str:postsId>/image',views.getImage,name="getImagePosts"),
    path('authors/<str:pk>/posts/<str:postsId>/comments',views.getComments,name="getComments"),
    path('authors/<str:pk>/posts/<str:postsId>/comments/<str:commentId>',views.getOneComment,name="getOneComment"),
    path('authors/<str:pk>/followers/',views.getFollowers,name="getFollowers"),
    path('authors/<str:pk>/followers/<str:foreignPk>',views.oneFollower,name="oneFollower"),
    path('authors/<str:pk>/liked',views.getLiked,name="getLiked"),
    path('authors/<str:pk>/posts/<str:postsId>/likes',views.getPostLikes,name="getPostsLikes"),
    path('authors/<str:pk>/inbox',views.getInbox,name="onesInbox"),
]

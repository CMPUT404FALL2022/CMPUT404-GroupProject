from django.urls import path
from . import views


urlpatterns = [
    # path("", views.authors, name="authors"),
    path('authors/',views.authorsList, name="authors-list"),
    path('authors/<str:pk>/',views.singleAuthor,name="singleAuthor"),
    path('authors/<str:pk>/posts/',views.Posts,name="onesPosts"),
    path('authors/<str:pk>/posts/<str:postsId>/',views.getPost,name="getPosts")
]

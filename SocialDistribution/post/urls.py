from django.urls import path
from . import views
urlpatterns = [
    path("posts", views.posts,name="posts-page"),
    path("home/<str:userId>",views.home_page,name="home-page"),
    path("create", views.create_post,name="create-page"),
]

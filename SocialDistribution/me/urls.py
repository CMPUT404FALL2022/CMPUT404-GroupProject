from django.urls import path
from . import views

urlpatterns = [

    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),
    path("authors/<str:userId>/profile/<str:postId>", views.my_profile_modify,name="modify-post-page"),
    path("authors/<str:userId>/information", views.myinfo,name="information-page"),
    
    path("authors/<str:userId>/informationedit", views.myinfoedit,name="informationedit-page"),

]


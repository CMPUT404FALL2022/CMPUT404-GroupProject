from django.urls import path
from . import views

urlpatterns = [

    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),
    path("authors/<str:userId>/information", views.myinfo,name="information-page"),

]


from django.urls import path
from . import views

urlpatterns = [

    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),
    path("authors/<str:userId>/information", views.myinfo,name="information-page"),
<<<<<<< Updated upstream
    path("authors/<str:userId>/informationedit", views.myinfoedit,name="informationedit-page"),
=======
    path("authors/<str:userId>/information_edit", views.myinfoedit,name="informationedit-page"),
>>>>>>> Stashed changes

]


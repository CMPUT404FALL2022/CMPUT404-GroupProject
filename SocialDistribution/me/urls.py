from django.urls import path
from . import views

urlpatterns = [
    # path('me/<str:userId>/', views.my_page),
    # path('me/<str:userId>/myPosts/', views.my_post_page),
    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),
    path("authors/<str:userId>/profile/<str:postId>", views.my_profile_modify,name="modify-post-page"),
]


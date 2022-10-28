from django.urls import path
from . import views


urlpatterns = [
    # path('me/<str:userId>/', views.my_page),
    # path('me/<str:userId>/myPosts/', views.my_post_page),
    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),

]


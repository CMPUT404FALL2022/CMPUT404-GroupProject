from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('me/<str:userId>/', views.my_page),
    path('me/<str:userId>/myPosts/', views.my_post_page),
]
=======
    # path('me/<str:userId>/', views.my_page),
    # path('me/<str:userId>/myPosts/', views.my_post_page),
    path("authors/<str:userId>/profile", views.my_profile,name="profile-page"),
    path("authors/<str:userId>/information", views.myinfo,name="information-page"),

]

>>>>>>> Stashed changes

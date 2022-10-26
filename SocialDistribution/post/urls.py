from django.urls import path
from . import views
urlpatterns = [
    path("authors/<str:userId>/posts",views.home_page,name="home-page"),
    path("authors/<str:userId>/posts/create", views.create_post,name="create-page"),
]

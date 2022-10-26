from django.urls import path
from . import views
urlpatterns = [
    path("<str:userId>",views.home_page,name="home-page"),
    path("<str:userId>/create", views.create_post,name="create-page"),
]

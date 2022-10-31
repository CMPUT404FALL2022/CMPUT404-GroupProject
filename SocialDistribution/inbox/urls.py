from django.urls import path
from . import views

urlpatterns = [
  path("authors/<str:userId>/inbox", views.my_inbox,name="inbox-page"),

]
from django.urls import path
from . import views

urlpatterns = [
  
  path("authors/<str:userId>/inbox", views.my_inbox,name="inbox-page"),
  path("authors/<str:userId>/search_result",views.search_result,name="search-result"),
  
]

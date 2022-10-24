from django.urls import path
from . import views

urlpatterns = [
    # path("", views.authors, name="authors"),
    path('authors/',views.authorsList, name="authors-list"),
    path('authors/<str:pk>/',views.singleAuthor,name="singleAuthor")
]
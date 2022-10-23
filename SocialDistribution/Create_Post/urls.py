from django.urls import path
from . import views

urlpatterns = [
  path('new_post/', views.create),
]
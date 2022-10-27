from django.urls import path
from . import views

urlpatterns = [
  path('inbox/', views.Inbox),
]
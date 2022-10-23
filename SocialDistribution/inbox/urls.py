from django.urls import path
from . import views

urlpatterns = [
  path('frinds/', views.create),
]
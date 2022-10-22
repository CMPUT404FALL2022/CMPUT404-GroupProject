from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.log_in),
    path("signup/", views.sign_up)
]
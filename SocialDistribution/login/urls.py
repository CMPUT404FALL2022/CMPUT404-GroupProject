from django.urls import path
from . import views

urlpatterns = [
    path("login", views.log_in,name="log_in_page"),
    path("signup", views.sign_up,name="sign_up_page")
]
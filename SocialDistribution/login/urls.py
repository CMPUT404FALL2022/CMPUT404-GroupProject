from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("login/", views.log_in, name="login"),
    path("signup/", views.sign_up, name="signup")
=======
    path("", views.log_in, name="login"),
    path("signup", views.sign_up, name="signup")
    
>>>>>>> main
]
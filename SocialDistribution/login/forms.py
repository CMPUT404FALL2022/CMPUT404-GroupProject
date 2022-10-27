from django import forms
from authors.models import single_author
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    # username = forms.CharField(max_length=255)
    # password = forms.CharField(max_length=255)
    class Meta:
        model = single_author
        fields = ['display_name','github','profileImage']

class newUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class LoginForm(forms.ModelForm):
    class Meta:
        model = single_author
        fields = ['username', 'password']
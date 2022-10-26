from django import forms
from authors.models import single_author

class SignUpForm(forms.ModelForm):
    # username = forms.CharField(max_length=255)
    # password = forms.CharField(max_length=255)
    class Meta:
        model = single_author
        fields = ['username', 'password','display_name']

class LoginForm(forms.ModelForm):
    class Meta:
        model = single_author
        fields = ['username', 'password']
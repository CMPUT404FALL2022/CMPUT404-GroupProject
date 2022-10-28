from django import forms
from authors.models import followRequest

class followRequestForm(forms.ModelForm):
    # username = forms.CharField(max_length=255)
    # password = forms.CharField(max_length=255)
    object = forms.CharField(max_length=255, required = True)

    class Meta:
        model = followRequest
        fields = ['object','summary']
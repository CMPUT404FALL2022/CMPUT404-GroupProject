from django import forms
from authors.models import followRequest
from authors.models import single_author

class followRequestForm(forms.ModelForm):
    # username = forms.CharField(max_length=255)
    # password = forms.CharField(max_length=255)
    object = forms.CharField(max_length=255, required = True)

    class Meta:
        model = followRequest
        fields = ['object','summary']


class EditForm(forms.ModelForm):

    class Meta:
        model = single_author
        fields=['display_name','github']

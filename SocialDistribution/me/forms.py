from django import forms
from authors.models import single_author

class EditForm(forms.ModelForm):

    class Meta:
        model = single_author
        fields=['password','display_name','github']

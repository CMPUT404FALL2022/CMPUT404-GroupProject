from django.forms import ModelForm
from authors.models import single_author

class SignUpForm(ModelForm):
    class Meta:
        model = single_author
        fields = '__all__'
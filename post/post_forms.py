from django import forms
from .models import Post, Comment
from authors.models import Followers
from django.db.models import Q


class post_form(forms.ModelForm):
    title = forms.CharField(label='title', 
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Please enter your title',
        })
    )

    description = forms.CharField(label='description',
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Please enter your description',
        })
    )
    content = forms.CharField(label='content', 
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'If you want to type something',

        })
    )

    Categories = forms.CharField(label='categories',
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder':"You can place your categories here." ,
            'rows':2,

        })
    )
    class Meta:
        model = Post
        fields = ['title', 'description', 'textType', 'content','contentType','Categories','visibility',"post_image"]
        

class Comment_form(forms.ModelForm):
    comment = forms.CharField(label='comment', 
        widget=forms.Textarea(attrs={
            'placeholder': 'Type in your comment here...',
        
        })
    )

    class Meta:
        model = Comment
        fields = ['comment', 'contentType']


# class Like_form(forms.ModelForm):
#     class Meta:
#         model = Like
#         fields = ['like']


class ExternalForm(forms.Form):
    
    title = forms.CharField(label='Title', 
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Please enter your title',
        })
    )
    
    description = forms.CharField(label='Description',
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Please enter your description',
        })
    )
    contentType_CHOICES =(
    ("text/plain", "Plaintext"),
    ("text/markdown", "Markdown"),
    ("image/png;base64", "png"),
    ("image/jpeg;base64", "jpeg")
    )
    contentType = forms.ChoiceField(choices = contentType_CHOICES)

    
    content = forms.CharField(label='Content', 
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder': 'If you want to type something',

        })
    )
    post_image = forms.ImageField()

    VISIBILITY_CHOICES = (("PUBLIC", "Public"), ("FRIENDS", "Friends"),("PRIVATE", "Specific friend"))
    visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES)

    
    unlisted = forms.BooleanField()


    group_CHOICES =(
    (11, "11"),
    (16, "16"),
    (18, "18"),
    )
    group = forms.ChoiceField(choices = group_CHOICES)



    Categories = forms.CharField(label='Categories',
        required = False,
        widget=forms.Textarea(attrs={
            'placeholder':"You can place your categories here." ,
            'rows':2,

        })
    )

class UserSelectionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        userId = kwargs.pop('userId')
        super(UserSelectionForm, self).__init__(*args, **kwargs)
        befriend_list = Followers.objects.filter(author__uuid = userId)
        true_friend_list = []
        true_friend_list_id_name = []
        for befriend in befriend_list:
        # if befriend.follower.uuid != userId:
            who_followed_me = Followers.objects.filter(Q(author__uuid = befriend.follower.uuid)& Q(follower__uuid = userId))

            if who_followed_me.count() > 0:
                true_friend_list.append(who_followed_me)

        for friend in true_friend_list:
            true_friend_list_id_name.append(friend[0].author.username)

        friendChoices = [("","")]

        for i in true_friend_list_id_name:
            temp = (i,i)
            friendChoices.append(temp)

        self.fields['Send_To'].choices = friendChoices

    Send_To = forms.ChoiceField()
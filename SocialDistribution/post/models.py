
from django.db import models
from authors.models import single_author

import uuid



# Create your models here.
class Post(models.Model):

    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False,unique=True)
    id = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200,null=True)
    origin = models.CharField(max_length=200,null=True)
    # url = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    content = models.CharField(max_length=256, null=True, blank=True)
    Categories = models.CharField(max_length=100, default="")
    CONTENT_CHOICES = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown"),
                       ("application/base64", "app"),
                       ("image/png;base64", "png"),
                       ("image/jpeg;base64", "jpeg")]
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICES,default = ("text/plain", "Plaintext"))
    TEXT_CHOICES = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown")]
    textType = models.CharField(max_length=30, choices=TEXT_CHOICES, default = ("text/plain", "Plaintext"))

    author = models.ForeignKey(single_author,related_name='posts',on_delete=models.CASCADE,blank=True, null=True)
    count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True, null=True)
    VISIBILITY_CHOICES = [("PUBLIC", "Public"), ("FRIENDS", "Friends"),
                          ("PRIVATE", "Specific friend")]
    visibility = models.CharField(max_length=7,
                                  choices=VISIBILITY_CHOICES,
                                  default="PUBLIC")
    #likes = models.IntegerField(default=0)
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    unlisted = models.BooleanField(default=False)
    # comments = models.ForeignKey(Comment,related_name='comment',on_delete=models.CASCADE,blank=True, null=True)
    # image_b64 = models.BinaryField(blank=True, null=True)
    def __str__(self):
        return f"{self.author}"
        
    def to_dict(self):
        return {
            "title": self.title,
            # "author": self.author.username,
            "description": self.description,
            "content": self.content,
            "contentType": self.contentType,
            "published": self.published.strftime("%Y-%m-%d %H:%M:%S"),
            "visibility": self.visibility,
            # "unlisted": self.unlisted,
            # "likes": self.likes,
            "comments": self.comments,
            "Categories": self.Categories
        }

# class Like(models.Model):
#     type = models.CharField(default='like', max_length=200)
#     summary = models.TextField()
#     author = models.ForeignKey(single_author, on_delete=models.CASCADE, blank=True, null=True)
#     object = models.CharField(max_length=200)
    

class Comment(models.Model):
    type = "comment"
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id = models.CharField(max_length=200, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(single_author,related_name='comment',on_delete=models.CASCADE,blank=True, null=True)
    comment = models.TextField(max_length=256, null=True, blank=True)
    CONTENT_CHOICES = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown")]
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICES,default = ("text/plain", "Plaintext"))
    published = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.comment} + {self.contentType} + {self.id}"



class Like(models.Model):
    type = models.CharField(default='like', max_length=200)
    summary = models.TextField(max_length=256, null=True, blank=True)
    # sender
    author = models.ForeignKey(single_author, on_delete=models.CASCADE, blank=True, null=True)
    object = models.CharField(max_length=200, null=True)


class Liked(models.Model): 
    type = models.CharField(default='liked', max_length=200)
    items = models.ManyToManyField(Like,blank=True)
    post = models.CharField(default='liked', max_length=200)

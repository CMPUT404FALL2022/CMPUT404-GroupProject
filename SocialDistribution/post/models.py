
from django.db import models
import uuid

# Create your models here.
class Post(models.Model):

    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    id = models.CharField(max_length=200,default = '')
    source = models.CharField(max_length=200,default = '')
    origin = models.CharField(max_length=200,default = '')
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
    textType = models.CharField(max_length=30, choices=TEXT_CHOICES, null=True, blank=True)

    # author = models.ForeignKey(to="authors.single_author", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True, null=True)
    VISIBILITY_CHOICES = [("PUBLIC", "Public"), ("FRIENDS", "Friends"),
                          ("PRIVATE", "Specific friend")]
    visibility = models.CharField(max_length=7,
                                  choices=VISIBILITY_CHOICES,
                                  default="PUBLIC")
    # likes = models.IntegerField(default=0)
    # post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    # image_b64 = models.BinaryField(blank=True, null=True)
    def __str__(self):
        return f"{self.title} + {self.uuid} + {self.description} + {self.contentType} + {self.published} + {self.visibility} + {self.Categories}"
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

class Like(models.Model):
    pass

class Comment(models.Model):
    type = "comment"
    comment = models.TextField(null=True, blank=True)
    contentType = "text/markdown"
    published = models.DateTimeField(auto_now_add=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)



from django.db import models
import uuid

# Create your models here.
class Post(models.Model):

    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200,null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    content = models.CharField(max_length=256, null=True, blank=True)
    # CONTENT_CHOICES = [("text/plain", "Plaintext"),
    #                    ("text/markdown", "Markdown"),
    #                    ("application/base64", "app"),
    #                    ("image/png;base64", "png"),
    #                    ("image/jpeg;base64", "jpeg")]
    # contentType = models.CharField(max_length=30, choices=CONTENT_CHOICES)
    # author = models.ForeignKey(to="authors.Author", on_delete=models.CASCADE)

    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    published = models.DateTimeField(auto_now_add=True, null=True)
    # post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    def __str__(self):
        return f"{self.title} + {self.uuid}"

class Like(models.Model):
    pass

class Comment(models.Model):
    pass


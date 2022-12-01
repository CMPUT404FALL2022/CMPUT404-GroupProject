from django.db import models
from uuid import uuid4
from authors.models import single_author
from post.models import Post

# # Create your models here.
# class InboxItem(models.Model):
#     class ItemTypeEnum(models.TextChoices):
#         POST = "post",
#         FOLLOW = "follow",
#         LIKE = "like",
#         COMMENT = "comment"

#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(single_author, on_delete=models.CASCADE) # guy who wrote the original post
#     item_id = models.CharField(max_length=200) # This could be the id of an item that isn't in our databse so can't foreign key
#     item_type = models.CharField(max_length=10, choices=ItemTypeEnum.choices)
#     item = models.TextField() # This is the content of the item


class Inbox(models.Model):
    type = models.CharField(default='inbox', max_length=200)
    author = models.ForeignKey(single_author, on_delete=models.CASCADE)
    items = models.ManyToManyField(Post, blank=True)
from distutils.errors import CompileError
from django.contrib import admin
from .models import Comment, Post, Like,Liked,Node

# Register your models here.
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Liked)
admin.site.register(Node)
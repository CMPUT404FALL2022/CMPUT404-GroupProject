from django.contrib import admin

from .models import single_author,Followers,FollowRequest

# Register your models here.
admin.site.register(single_author)
admin.site.register(FollowRequest)
admin.site.register(Followers)

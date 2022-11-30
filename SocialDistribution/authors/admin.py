from django.contrib import admin

from .models import single_author,Followers

# Register your models here.
admin.site.register(single_author)
# admin.site.register(followRequest)
admin.site.register(Followers)

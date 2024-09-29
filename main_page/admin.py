from django.contrib import admin
from .models import Story, Post, Following, CustomUser

# Register your models here.
admin.site.register(Story)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(CustomUser)

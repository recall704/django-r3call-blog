#coding:utf-8
from django.contrib import admin


from .models import Post, Category, FriendLink

admin.site.register(Post)

admin.site.register(Category)

admin.site.register(FriendLink)

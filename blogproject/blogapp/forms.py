#coding:utf-8
from django import forms
from .models import *


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','category','tags','content')
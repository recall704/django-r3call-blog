#coding:utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('blogapp.views',
    url(r"^$", "index", name="index"),
    url(r"^post/(?P<pk>\d+)/", "post", name="post"),
    url(r"^category/(?P<pk>\d+)/$", "category", name="category"),
)
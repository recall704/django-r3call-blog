#coding:utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('blogapp.views',
    url(r"^$", "index", name="index"),
    url(r"^about/$", "about", name="about"),
    url(r"^post/(?P<pk>\d+)/", "post",name="post_default"),
    url(r"^post/(?P<pk>\d+)/(?P<title>.+)/$", "post", name="post"),
    url(r"^category/(?P<pk>\d+)/$", "category"),
    url(r"^category/(?P<pk>\d+)/(?P<name>.+)/$", "category", name="category"),
    url(r"^tag/(?P<tag_id>\d+)/$", "tag", name="tag"),

    url(r"^add/$", "add", name="add"),
    url(r"^edit/(?P<pk>\d+)/$", "edit", name="edit"),
    url(r"^ajax_markdown_preview/$", "ajax_markdown_preview", name="ajax_markdown_preview"),
)
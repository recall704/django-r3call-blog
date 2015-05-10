from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blogproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'blogapp.views.index', name='home'),
    url(r'^xxoo123/', include(admin.site.urls)),
    url(r'^blog/', include('blogapp.urls')),
)

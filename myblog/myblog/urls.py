#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blogapp.views.index', name='home'),
    
    url(r'^blog/', include('blogapp.urls')),
    # url(r'^redactor/', include('redactor.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

    url(r'^admin/', include(admin.site.urls)),
)


# import 项目setting

if settings.DEBUG:

    urlpatterns += patterns('',

        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    )
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'act.resources.views.resource_list', name='resource_list'),
    url(r'^(?P<slug>[\w\-]+)/$', 'act.resources.views.resource_detail', name='resource_detail'),
)
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'act.events.views.event_index', name='event_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w\-]+)/$', 'act.events.views.event_detail', name='event_detail'),
)
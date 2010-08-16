from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'act.events.views.event_index', name='event_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w\-]+)/$', 'act.events.views.event_detail', name='event_detail'),
    
    url(r'^recent/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'act.events.views.event_recent_archive'),
    url(r'^recent/(?P<year>\d{4})/(?P<month>\d{2})/$', 'act.events.views.event_recent_archive'),
    url(r'^recent/(?P<year>\d{4})/$', 'act.events.views.event_recent_archive'),
    url(r'^recent/$', 'act.events.views.event_recent_archive', name='event_recent_archive'),
    
    url(r'^upcoming/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'act.events.views.event_upcoming_archive'),
    url(r'^upcoming/(?P<year>\d{4})/(?P<month>\d{2})/$', 'act.events.views.event_upcoming_archive'),
    url(r'^upcoming/(?P<year>\d{4})/$', 'act.events.views.event_upcoming_archive'),
    url(r'^upcoming/$', 'act.events.views.event_upcoming_archive', name='event_upcoming_archive'),
    
)
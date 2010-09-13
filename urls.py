from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from act import feeds
from act.hello.views import Hello

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<year>\d{4})/(?P<slug>[0-9a-zA-Z_\-]+)/$', 'act.views.post_detail', name='post_detail'),
    url(r'^blog/', include('blogdor.urls')),
    url(r'^contact/', Hello()),
    url(r'^events/', include('act.events.urls')),
    url(r'^resources/', include('act.resources.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^$', 'act.views.index', name='index'),
)

# feeds
urlpatterns += patterns('',
    url(r'^feeds/events/recent/$', feeds.RecentEventsFeed(), name='feed_recent_events'),
    url(r'^feeds/events/upcoming/$', feeds.UpcomingEventsFeed(), name='feed_upcoming_events'),
    url(r'^feeds/blog/$', feeds.LatestPosts(), name='feed_latest_posts'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

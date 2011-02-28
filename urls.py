from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.core.mail import send_mail
from act import feeds
from act.hello.views import Hello
from cloudmailin.views import MailHandler

admin.autodiscover()

def postbymail(**kwargs):
    
    def link_sub(match):
        groups = match.groups()
        return "([%s](%s))" % (BLANK_RE.sub(' ', groups[0]), groups[1])

    sender = kwargs['from']
    title = kwargs['subject']
    text = kwargs['plain']
    
    text = text.replace('\x3D\x0A', '')
    text = text.replace('\x3D\x39\x32', "'")
    text = text.replace('   - ', '   * ')
    text = LINK_RE.sub(link_sub, text)
        
    try:
        
        author = User.objects.get(email=sender)
        
        post = Post.objects.create(
            title=title,
            slug=slugify(title),
            author=author,
            content=text,
            excerpt=''
        )
        
        send_mail(
            subject='[TransparencyCaucus] New blog post created',
            message='http://transparencycaucus.org/admin/blogdor/post/%i/\n\n%s' % (post.pk, text),
            from_email='contact@sunlightfoundation.com',
            recipient_list=[author.email],
            fail_silently=True
        )
        
    except User.DoesNotExist:
        send_mail(
            subject='[TransparencyCaucus] Sorry, unable to create new blog post',
            message='%s' % text,
            from_email='contact@sunlightfoundation.com',
            recipient_list=[sender],
            fail_silently=True
        )

mail_handler = MailHandler()
mail_handler.register_address(
    '086724d946a97d966551@cloudmailin.net',
    '7eeb8b1cc3dc07d24f1e',
    postbymail,
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<year>\d{4})/(?P<slug>[0-9a-zA-Z_\-]+)/$', 'act.views.post_detail', name='post_detail'),
    url(r'^blog/postbymail/$', mail_handler),
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

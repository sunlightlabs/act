from django.shortcuts import get_object_or_404, render_to_response
from act.events.models import Event
from act.tweets.models import Tweet
from blogdor.models import Post
from feedinator.models import FeedEntry
import re

SLUG_RE = re.compile(r"(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[0-9a-zA-Z\-_]+)")

#
# this is really hacky using feedinator
#

def add_slug(post):
    match = SLUG_RE.search(post.link)
    post.slug = match.groupdict()['slug'] if match else None
    return post
    
# real views

def index(request):
    posts = Post.objects.published()[:2]
    upcoming_events = Event.objects.upcoming()[:3]
    tweets = Tweet.objects.filter(timeline__slug='act')[:4]
    return render_to_response('index.html', {
        'posts': posts,
        'upcoming_events': upcoming_events,
        'tweets': tweets,
    })

def post_detail(request, year, slug):
    data = {
        'post': add_slug(get_object_or_404(FeedEntry, link__icontains=slug)),
        'entries': (add_slug(e) for e in FeedEntry.objects.all()[:10]),
    }
    return render_to_response('blog/post_detail.html', data)
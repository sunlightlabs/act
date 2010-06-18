from django.shortcuts import get_object_or_404, render_to_response
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
    data = {
        'latest_post': add_slug(FeedEntry.objects.latest('date_published')),
    }
    return render_to_response('index.html', data)

def post_detail(request, year, slug):
    data = {
        'post': get_object_or_404(FeedEntry, link__icontains=slug),
    }
    return render_to_response('blog/post_detail.html', data)
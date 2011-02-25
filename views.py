from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from act.events.models import Event
from act.tweets.models import Tweet
from blogdor.models import Post
from feedinator.models import FeedEntry
import re

# for cloudmailin
BLANK_RE = re.compile(r'\s+')
LINK_RE = re.compile(r'\((.*?)<(.*?)>(.*?)\)', re.S)

# for slug urls
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
    posts = Post.objects.published()[:10]
    upcoming_events = Event.objects.upcoming()[:3]
    tweets = Tweet.objects.filter(timeline__slug='act')[:4]
    return render_to_response('index.html', {
        'posts': posts,
        'upcoming_events': upcoming_events,
        'tweets': tweets,
    }, context_instance=RequestContext(request))

def post_detail(request, year, slug):
    data = {
        'post': add_slug(get_object_or_404(FeedEntry, link__icontains=slug)),
        'entries': (add_slug(e) for e in FeedEntry.objects.all()[:10]),
    }
    return render_to_response('blog/post_detail.html', data)

# cloudmailin receiver

@csrf_exempt
def receive_email(request):

    def link_sub(match):
        groups = match.groups()
        return "([%s](%s))" % (BLANK_RE.sub(' ', groups[0]), groups[1])

    if request.method == "POST" and "signature" in request.POST:
        
        try:
        
            sender = request.POST['from']
            title = request.POST['subject']
            text = request.POST['plain']
            
            author = User.objects.get(email=sender)
            
            text = text.replace('\x3D\x0A', '')
            text = text.replace('\x3D\x39\x32', "'")
            text = text.replace('   - ', '   * ')
            text = LINK_RE.sub(link_sub, text)
            
            post = Post.objects.create(
                title=title,
                slug=slugify(title),
                author=author,
                content=text,
                excerpt=''
            )
            
            return HttpResponse('')
            
        except User.DoesNotExist:
            print "author does not match!!!"
    
    return HttpResponseRedirect('/')
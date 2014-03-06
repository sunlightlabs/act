from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from act.tweets.models import Timeline, Tweet
import datetime
import requests

def parse_datetime(s):
    fmt = "%a %b %d %H:%M:%S +0000 %Y"
    return datetime.datetime.strptime(s, fmt)

def load_json(url, timeline):

    auth = (settings.FOAUTH_USER, settings.FOAUTH_PASS)
    tweets = requests.get(url, auth=auth).json()

    for tweet in tweets:

        if not Tweet.objects.filter(id=tweet['id']).exists():

            t = Tweet(
                id=tweet['id'],
                text=tweet['text'],
                created_at=parse_datetime(tweet['created_at']),
                name=tweet['user']['name'],
                screen_name=tweet['user']['screen_name'],
                timeline=timeline,
            )
            t.save()

class Command(BaseCommand):
    args = '<timeline_slug>'
    help = ''

    def handle(self, slug=None, *args, **kwargs):

        if slug:

            try:
                tl = Timeline.objects.get(slug=slug)
            except Timeline.DoesNotExist:
                raise CommandError("'%s' is not a timeline" % slug)

            if tl.feed_type == 'json':
                load_json(tl.feed_url, tl)
            else:
                raise CommandError('RSS/Atom feeds are not supported')

        else:

            timelines = Timeline.objects.all()

            if not timelines:
                print "No available timelines"

            for tl in timelines:
                print u"[%s] %s" % (tl.slug, tl.title)

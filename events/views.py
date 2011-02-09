from django.db.models import Min
from django.shortcuts import render_to_response
from django.views.generic import date_based
from django.views.generic import list_detail
from tagging.models import Tag, TaggedItem
from act.events.models import Event
from act.resources.models import Resource
from blogdor.models import Post
import datetime

def event_index(request):
    data = {
        'upcoming': Event.objects.upcoming()[:3],
        'recent': Event.objects.recent()[:2],
        'tags': Tag.objects.usage_for_model(Event),
    }
    return render_to_response('events/index.html', data)

def event_archive(request, year=None):
    this_year = datetime.datetime.today().year
    min_year = Event.objects.aggregate(min_date=Min('start_date'))['min_date'].year
    if not year:
        year = this_year
    qs = Event.objects.filter(start_date__year=year, is_public=True)
    return date_based.archive_year(
                request,
                year=year,
                make_object_list=True,
                date_field='start_date',
                allow_future=True,
                template_name='events/event_archive.html',
                template_object_name='event',
                queryset=qs,
                extra_context={
                    'years': [y for y in range(min_year, this_year + 1)],
                })

def event_detail(request, year, month, day, slug):
    # try:
    #     e = Event.objects.get(slug=slug)
    #     print e.tags
    #     related_posts = TaggedItem.objects.get_union_by_model(Post, e.tags)
    # except Event.DoesNotExist:
    #     related_posts = None
    # print "!!!", related_posts
    return date_based.object_detail(
                request,
                year=year,
                month=month, month_format='%m',
                day=day,
                slug=slug,
                date_field='start_date',
                queryset=Event.objects.all(),
                extra_context={
                    'related_posts': None,
                })
from django.db.models import Min
from django.shortcuts import render_to_response
from django.views.generic import date_based
from tagging.models import Tag
from act.events.models import Event
import datetime


def event_index(request):
    now = datetime.datetime.now()
    data = {
        'upcoming': Event.objects.upcoming()[:3],
        'recent': Event.objects.recent().filter(start_date__year=now.year),
        'tags': Tag.objects.usage_for_model(Event),
        'year': now.year
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
    return date_based.object_detail(
                request,
                year=year,
                month=month, month_format='%m',
                day=day,
                slug=slug,
                date_field='start_date',
                allow_future=True,
                queryset=Event.objects.filter(is_public=True))

from django.shortcuts import render_to_response
from django.views.generic import date_based
from django.views.generic import list_detail
from tagging.models import Tag
from act.events.models import Event

def event_index(request):
    data = {
        'upcoming': Event.objects.upcoming()[:3],
        'recent': Event.objects.recent()[:2],
        'tags': Tag.objects.usage_for_model(Event),
    }
    return render_to_response('events/index.html', data)


def event_recent_archive(request, year=None, month=None, day=None):
    return event_archive(request, Event.objects.recent(), year, month, day)

def event_upcoming_archive(request, year=None, month=None, day=None):
    return event_archive(request, Event.objects.upcoming(), year, month, day)

def event_archive(request, qs, year=None, month=None, day=None):
    if day:
        print "!!! day"
        return date_based.archive_day(
                    request,
                    year=year,
                    month=month,
                    day=day,
                    month_format='%m',
                    date_field='start_date',
                    allow_future=True,
                    template_name='events/event_archive.html',
                    template_object_name='event',
                    queryset=qs)
    elif month:
        print "!!! month"
        return date_based.archive_month(
                    request,
                    year=year,
                    month=month,
                    month_format='%m',
                    date_field='start_date',
                    allow_future=True,
                    template_name='events/event_archive.html',
                    template_object_name='event',
                    queryset=qs)
    elif year:
        print "!!! year"
        return date_based.archive_year(
                    request,
                    year=year,
                    make_object_list=True,
                    date_field='start_date',
                    allow_future=True,
                    template_name='events/event_archive.html',
                    template_object_name='event',
                    queryset=qs)
    else:
        print "!!! index"
        return date_based.archive_index(
                    request,
                    date_field='start_date',
                    allow_future=True,
                    template_name='events/event_archive.html',
                    template_object_name='event_list',
                    queryset=qs)

def event_detail(request, year, month, day, slug):
    return date_based.object_detail(
                request,
                year=year,
                month=month, month_format='%m',
                day=day,
                slug=slug,
                date_field='start_date',
                queryset=Event.objects.all())
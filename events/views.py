from django.shortcuts import render_to_response
from django.views.generic import date_based
from django.views.generic import list_detail
from act.events.models import Event

def event_index(request):
    data = {
        'upcoming': Event.objects.upcoming()[:3],
        'recent': Event.objects.recent()[:2],
    }
    return render_to_response('events/index.html', data)

def event_archive(request, year=None, month=None, day=None):
    return list_detail.object_list(
                request,
                queryset=Event.objects.all())

def event_detail(request, year, month, day, slug):
    return date_based.object_detail(
                request,
                year=year,
                month=month, month_format='%m',
                day=day,
                slug=slug,
                date_field='start_date',
                queryset=Event.objects.all())
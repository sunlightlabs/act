from django.views.generic.list_detail import object_detail, object_list
from act.resources.models import Resource

def resource_list(request):
    return object_list(
                request,
                queryset=Resource.objects.all())

def resource_detail(request, slug):
    return object_detail(
                request,
                queryset=Resource.objects.all(),
                slug=slug)
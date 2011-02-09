from django.views.generic.list_detail import object_detail, object_list
from act.resources.models import Topic

def resource_list(request):
    return object_list(
                request,
                queryset=Topic.objects.all())

def resource_detail(request, slug):
    return object_detail(
                request,
                queryset=Topic.objects.all(),
                slug=slug)
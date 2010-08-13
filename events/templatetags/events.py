from act.events.models import Event
from django import template
from django.template import Context
import re

register = template.Library()

class EventsContextNode(template.Node):

    def __init__(self, queryset, var_name):
        self.queryset = queryset
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = self.queryset
        return ''

class EventsTemplateNode(template.Node):
    
    def __init__(self, queryset, nodelist):
        self.queryset = queryset
        self.nodelist = nodelist
        
    def render(self, context):
        content = ''
        for event in self.queryset:
            content += self.nodelist.render(Context({'event': event})) + '\n'
        return content

@register.tag(name="events")
def do_events(parser, token, queryset=None):
    
    m = re.search(r'(?P<tag>\w+)(?: (?P<count>\d{1,4}))?(?: as (?P<var_name>\w+))?', token.contents)
    args = m.groupdict()
    
    if not queryset:
        queryset = Event.objects.all()
    
    if args['count']:
        try:
            queryset = queryset[:int(args['count'])]
        except ValueError:
            raise template.TemplateSyntaxError, "count argument must be an integer"
    
    if args['var_name']:
        return EventsContextNode(queryset, args['var_name'])
        
    else:
        nodelist = parser.parse(('end%s' % args['tag'],))
        parser.delete_first_token()
        return EventsTemplateNode(queryset, nodelist)

@register.tag(name="recentevents")
def do_recent_events(parser, token):    
    qs = Event.objects.recent()
    return do_events(parser, token, qs)

@register.tag(name="upcomingevents")
def do_upcoming_events(parser, token):
    qs = Event.objects.upcoming()
    return do_events(parser, token, qs)
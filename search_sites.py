from haystack import site
from haystack.fields import CharField, DateTimeField
from haystack.indexes import SearchIndex
from blogdor.models import Post
from act.events.models import Event
from act.resources.models import Topic

class PostIndex(SearchIndex):
    text = CharField(document=True, model_attr='content', use_template=True)
    title = CharField(model_attr='title') 
    slug = CharField(model_attr='slug')
    date_published = DateTimeField(model_attr='date_published')
    type = CharField(default='post')
    
    def get_queryset(self):
        return Post.objects.published()
        
site.register(Post, PostIndex)


class TopicIndex(SearchIndex):
    text = CharField(document=True, model_attr='content', use_template=True)
    title = CharField(model_attr='title')
    slug = CharField(model_attr='slug')
    type = CharField(default='topic')
    
    def get_queryset(self):
        return Topic.objects.all()

site.register(Topic, TopicIndex)


class EventIndex(SearchIndex):
    text = CharField(document=True, model_attr='content', use_template=True)
    title = CharField(model_attr='title')
    slug = CharField(model_attr='slug')
    url = CharField(model_attr='get_absolute_url')
    type = CharField(default='event')
    
    def get_queryset(self):
        return Event.objects.filter(is_public=True)

site.register(Event, EventIndex)
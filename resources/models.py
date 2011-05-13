from django.db import models
from act.events.models import Event
from blogdor.models import Post
from tagging.models import Tag, TaggedItem

RESOURCE_TYPES = (
    ('d', 'document'),
    ('l', 'link'),
)

class Topic(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="resources", blank=True, null=True)
    
    class Meta:
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title
    
    def posts(self):
        if self.tags:
            return TaggedItem.objects.get_by_model(Post, self.tags.all())
    
    def events(self):
        if self.tags:
            qs = TaggedItem.objects.get_by_model(Event, self.tags.all())
            return qs.filter(is_public=True).order_by('-start_date', '-start_time')

class Resource(models.Model):
    topic = models.ForeignKey(Topic, related_name='resources')
    type = models.CharField(max_length=1, choices=RESOURCE_TYPES)
    url = models.URLField(verify_exists=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=100)
    
    class Meta:
        ordering = ('-order',)
    
    def __unicode__(self):
        return self.title
    
from django.db import models
from blogdor.models import Post
from tagging.models import Tag, TaggedItem

class Resource(models.Model):
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
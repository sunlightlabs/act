from django.db import models

FEED_TYPES = (
    ('json', 'JSON'),
    ('rss', 'RSS/Atom'),
)

class Timeline(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    feed_type = models.CharField(max_length=8, choices=FEED_TYPES)
    feed_url = models.URLField(verify_exists=False)
    
    class Meta:
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title

class Tweet(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    text = models.CharField(max_length=225)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=128)
    screen_name = models.CharField(max_length=128)
    
    timeline = models.ForeignKey(Timeline, related_name='tweets')
    
    class Meta:
        ordering = ('-created_at',)
    
    def __unicode__(self):
        return u"%s: %s" % (self.screen_name, self.text)
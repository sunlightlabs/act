from django.core.urlresolvers import reverse
from django.db import models
import datetime

class EventManager(models.Manager):
    
    def recent(self):
        now = datetime.datetime.now()
        return Event.objects.filter(
            start_date__lte=now.date(), start_time__lte=now.time(), is_public=True
        ).order_by('-start_date')
    
    def upcoming(self):
        now = datetime.datetime.now()
        return Event.objects.filter(
            start_date__gte=now.date(), start_time__gt=now.time(), is_public=True
        ).order_by('start_date')

class Event(models.Model):
    objects = EventManager()
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    video_url = models.URLField(verify_exists=False, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    
    class Meta:
        ordering = ('-start_date', '-start_time')
    
    def __unicode__(self):
        return u"%s %s" % (self.start_date, self.title)
    
    def get_absolute_url(self):
        return reverse('event_detail', args=(
            '%s' % self.start_date.year,
            '%02d' % self.start_date.month,
            '%02d' % self.start_date.day,
            self.slug
        ))

class PressRelease(models.Model):
    event = models.ForeignKey(Event, related_name="press_releases")
    released_by = models.CharField(max_length=255)
    url = models.URLField(verify_exists=False)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    
    class Meta:
        ordering = ('released_by',)
    
    def __unicode__(self):
        return u"%s - %s" % (self.event, self.released_by) 
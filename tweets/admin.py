from act.tweets.models import Timeline, Tweet
from django.contrib import admin

class TimelineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Timeline, TimelineAdmin)

class TweetAdmin(admin.ModelAdmin):
    list_display = ('screen_name','created_at','text')
    list_display_links = ('text',)
    list_filter = ('timeline',)
    
admin.site.register(Tweet, TweetAdmin)
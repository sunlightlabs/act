from django.contrib.syndication.views import Feed
from act.events.models import Event
from blogdor.models import Post

# event feeds

class EventsFeed(Feed):

    description_template = "feeds/events.html"
    item_author_name = "The Advisory Committee on Transparency"
    
    def item_pubdate(self, item):
        return item.timestamp
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_title(self, item):
        return item.title

class RecentEventsFeed(EventsFeed):
    title = "Recent Transparency Caucus events"
    link = "/events/recent/"
    description = "Recent Transparency Caucus events"
    
    def items(self):
        return Event.objects.recent()[:10]

class UpcomingEventsFeed(EventsFeed):
    title = "Upcoming Transparency Caucus events"
    link = "/events/upcoming/"
    description = "Upcoming Transparency Caucus events"
    
    def items(self):
        return Event.objects.upcoming()[:10]

# blog feeds

class LatestPosts(Feed):
    title = "Recent Advisory Committee on Transparency blog posts"
    link = "/blog/"
    description = "Recent Transparency Caucus blog posts"
    
    description_template = "feeds/posts.html"
    
    def items(self):
        return Post.objects.published()[:10]
        
    def item_author_name(self, post):
        if post.author:
            return post.author.get_full_name()
        return "Anonymous"

    def item_pubdate(self, post):
        return post.date_published
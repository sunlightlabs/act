from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from blogdor.models import Post
from pymongo.connection import Connection
import datetime

class Command(BaseCommand):
    args = '<timeline_slug>'
    help = ''
    
    def handle(self, slug=None, *args, **kwargs):
        
        conn = Connection()
        
        users = {
            'Daniel Schuman': User.objects.get(username='dschuman'),
            'John Wonderlich': User.objects.get(username='jwonderlich'),
            'enaing': User.objects.get(username='enaing'),
            'Melanie Buck': User.objects.get(username='mbuck'),
            'Nicko Margolies': User.objects.get(username='nmargolies'),
            'Alexis Rudakewych': User.objects.get(username='arudakewych'),
        }

        for doc in conn['openhouse']['blog'].find():
            
            tags = ", ".join(['"%s"' % t for t in doc['tags']])
            print tags
            
            p = Post(
                id=doc['ID'],
                title=doc['post_title'],
                slug=slugify(doc['post_title']),
                author=users[doc['user_login']],
                last_updated=doc['post_modified'] or doc['post_date'],
                date_published=doc['post_date'],
                timestamp=doc['post_date'],
                is_published=True,
            )
            
            p.tags = tags
            
            p.content = unicode(doc['post_content'], 'utf8', 'ignore')
            p.content_markup_type = 'markdown'
            
            p.excerpt = unicode(doc['post_excerpt'], 'utf8', 'ignore') or ''
            p.excerpt_markup_type = 'markdown'
            
            p.save()
            
            print p.title

from django.contrib import admin
from act.resources.models import Topic, Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('type','title')
    list_display_links = ('title',)

admin.site.register(Resource, ResourceAdmin)

class ResourceInline(admin.StackedInline):
    model = Resource

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ResourceInline,)

admin.site.register(Topic, TopicAdmin)
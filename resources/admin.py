from django.contrib import admin
from act.resources.models import Topic, Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('type','title','order')
    list_display_links = ('title',)
    list_editable = ('order',)
    list_filter = ('topic',)

admin.site.register(Resource, ResourceAdmin)

class ResourceInline(admin.StackedInline):
    model = Resource

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ResourceInline,)

admin.site.register(Topic, TopicAdmin)
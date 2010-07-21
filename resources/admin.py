from django.contrib import admin
from act.resources.models import Resource

class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Resource, ResourceAdmin)
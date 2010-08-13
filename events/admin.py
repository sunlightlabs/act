from django.contrib import admin
from act.events.models import Event, PressRelease

class PressReleaseInline(admin.TabularInline):
    model = PressRelease
    exclude = ('timestamp',)

class EventAdmin(admin.ModelAdmin):
    inlines = (PressReleaseInline,)
    exclude = ('timestamp',)
    list_display = ('title','start_date','location','is_public')
    list_display_links = ('title',)
    list_editable = ('is_public',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Event, EventAdmin)
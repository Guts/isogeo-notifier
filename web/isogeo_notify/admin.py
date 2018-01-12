from django.contrib import admin
from .models import (Metadata, MetadataType, CrawlerHistory, State, Workgroup)


class MetadataAdmin(admin.ModelAdmin):
    readonly_fields = ('mdid',)
    # FIELDS DISPLAY and FILTERS
    list_display = ("isogeo_uuid", "title", "name")
    list_filter = ("md_dt_crea", "workgroup", "md_type", "state")
    search_fields = ("title", "abstract", "name")
    date_hierarchy = "md_dt_crea"
    ordering = ('-md_dt_crea',)


# REGISTERING and DISPLAY
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(MetadataType)
admin.site.register(CrawlerHistory)
admin.site.register(State)
admin.site.register(Workgroup)

from django.contrib import admin
from .models import Zone


# Register your models here.
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "id",
        "zone_id",
        "description",
        "updated_at",
        "created_at",
        "deleted_at",
    ]
    readonly_fields: list[str] = [
        "id",
        "updated_at",
        "created_at",
        "deleted_at",
    ]
    list_filter: list[str] = ["created_at", 'zone_id']

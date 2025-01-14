from django.contrib import admin
from .models import Zone, ClusterProvider, ClusterCapacity, Quota


class ClusterProviderInline(admin.StackedInline):
    model = ClusterProvider
    can_delete = False
    verbose_name_plural = "cluster_provider"


class ClusterCapacityInline(admin.StackedInline):
    model = ClusterCapacity
    can_delete = False
    verbose_name_plural = "cluster_capacity"


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
        "capacity"
    ]
    readonly_fields: list[str] = [
        "id",
        "updated_at",
        "created_at",
        "deleted_at",
    ]
    list_filter: list[str] = ["created_at", "zone_id"]
    inlines = [ClusterProviderInline, ClusterCapacityInline]

admin.site.register(Quota)
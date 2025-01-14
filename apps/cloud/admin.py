from django.contrib import admin

from .models import ClusterCapacity, ClusterProvider, Node, Quota, ReservePlan, Zone


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
        "capacity",
    ]
    readonly_fields: list[str] = [
        "id",
        "updated_at",
        "created_at",
        "deleted_at",
    ]
    list_filter: list[str] = ["created_at", "zone_id"]
    inlines = [ClusterProviderInline, ClusterCapacityInline]


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "id",
        "zone",
        "project",
        "quota_cpu",
        "quota_gpu",
        "quota_mem",
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
    list_filter: list[str] = ["created_at", "project"]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "id",
        "zone",
        "cluster_provider",
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
    list_filter: list[str] = ["created_at", "zone"]


@admin.register(ReservePlan)
class ReservePlanAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "id",
        "zone",
        "project",
        "reserve_cpu",
        "reserve_gpu",
        "reserve_mem",
        "reserve_start",
        "reserve_end",
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
    list_editable = ["reserve_start", "reserve_end"]
    list_filter: list[str] = ["created_at", "project"]

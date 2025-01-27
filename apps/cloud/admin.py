from django.contrib import admin
from django.db import models
from .models import (
    ClusterProvider,
    Node,
    Quota,
    ReservePlan,
    Zone,
    TaskQueue,
    ZoneCapacityStatic,
)
from apps.storage.models import Class
from unfold.admin import StackedInline, TabularInline
from unfold.admin import ModelAdmin


class ClusterProviderInline(StackedInline):
    model = ClusterProvider
    can_delete = False
    verbose_name_plural = "cluster_provider"


class ClusterClassInline(TabularInline):
    model = Class
    extra = 0


class NodeInline(TabularInline):
    model = Node
    extra = 0


# Register your models here.
@admin.register(Zone)
class ZoneAdmin(ModelAdmin):
    def node_count(self, obj) -> int:
        return obj.nodes.count()

    def resource_cap(self, obj) -> int:
        return (
            f"{obj.nodes.aggregate(models.Sum('node_cpu')).get('node_cpu__sum') or 0}C/"
            f"{obj.nodes.aggregate(models.Sum('node_mem')).get('node_mem__sum') or 0}Mem/"
            f"{obj.nodes.aggregate(models.Sum('node_gpu')).get('node_gpu__sum') or 0}GPU"
        )

    list_display: list[str] = [
        "id",
        "zone_id",
        "description",
        "node_count",
        "resource_cap",
        "updated_at",
        "created_at",
    ]
    readonly_fields: list[str] = [
        "id",
        "updated_at",
        "created_at",
    ]
    list_filter: list[str] = ["created_at", "zone_id"]
    inlines = [
        ClusterProviderInline,
        ClusterClassInline,
        NodeInline,
    ]


class TaskQueueInline(TabularInline):
    model = TaskQueue
    extra = 0


@admin.register(Quota)
class QuotaAdmin(ModelAdmin):
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
    inlines = [TaskQueueInline]


@admin.register(Node)
class NodeAdmin(ModelAdmin):
    def _capacity(self, obj) -> str:
        return f"{obj.node_cpu}C/{obj.node_mem}Mem/{obj.node_gpu}GPU"

    list_display: list[str] = [
        "id",
        "zone",
        "node_name",
        "node_ip",
        "node_status",
        "_capacity",
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
class ReservePlanAdmin(ModelAdmin):
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


@admin.register(ZoneCapacityStatic)
class ZoneCapacityStaticAdmin(ModelAdmin):
    list_display: list[str] = [
        "id",
        "zone",
        "cpu_capacity",
        "gpu_capacity",
        "mem_capacity",
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
    list_editable = ["cpu_capacity", "gpu_capacity", "mem_capacity"]

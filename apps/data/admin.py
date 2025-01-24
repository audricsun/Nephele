from django.contrib import admin
from typing import List
from .models import Layout, Dataset, Mount
from unfold.admin import ModelAdmin


@admin.register(Dataset)
class DatasetAdmin(ModelAdmin):
    list_display: List[str] = [
        "id",
        "display_name",
        "storage_path",
        "default_mount",
        "quota",
        "limit_size",
        "used_size",
        "access_level",
        "updated_at",
        "created_at",
    ]
    readonly_fields: List[str] = ["deleted_at", "created_at", "updated_at"]


@admin.register(Mount)
class MountsAdmin(ModelAdmin):
    list_display: list[str] = [
        "id",
        "dataset",
        "mount",
        "layout",
    ]


class MountsInLine(admin.TabularInline):
    model = Mount
    extra = 0


def format(input: str) -> str:
    return f'<div style="width: 100px; word-wrap: break-word">{input}</div>'


@admin.register(Layout)
class LayoutAdmin(ModelAdmin):
    def mounts(self, obj) -> list[str]:
        return ",".join([f"{m}" for m in obj.mounts.all()])

    def heritaged_mounts(self, obj) -> List[str]:
        return ",".join([f"{m}" for m in obj.list_parent_mounts()])

    def all_mounts(self, obj) -> list[str]:
        return ",".join([f"{m}" for m in obj.list_mounts()])

    def zone_info(self, obj) -> str:
        return obj.zone.zone_id

    inlines: list[type[MountsInLine]] = [MountsInLine]
    list_display: list[str] = [
        "id",
        "display_name",
        "zone_info",
        "mounts",
        "heritaged_mounts",
        "all_mounts",
        "created_at",
        "updated_at",
    ]
    search_fields = ("display_name",)
    list_editable = ("display_name",)

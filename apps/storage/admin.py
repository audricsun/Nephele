from django.contrib import admin
from typing import List
from .models import Class, StorageCapacity
from apps.data.models import Dataset
from unfold.admin import ModelAdmin

from unfold.admin import TabularInline


class DatasetInLine(TabularInline):
    model = Dataset
    extra = 0
    tab = True

    list_display: List[str] = [
        "id",
        "display_name",
        "storage_path",
        "quota",
        "limit_size",
        "used_size",
        "access_level",
        "updated_at",
        "created_at",
    ]


class QuotaInLine(TabularInline):
    model = StorageCapacity
    extra = 0


@admin.register(StorageCapacity)
class QuotaAdmin(ModelAdmin):
    def provider(self, obj) -> str:
        return str(obj.provider)

    def datasets(self, obj) -> str:
        return [f"{dataset}" for dataset in obj.datasets.all()]

    list_display: List[str] = [
        "id",
        "owner",
        "available",
        "used",
        "limit",
        "provider",
        "datasets",
    ]
    inlines = [DatasetInLine]
    readonly_fields: List[str] = ["deleted_at", "created_at", "updated_at"]


@admin.register(Class)
class ClassAdmin(ModelAdmin):
    def list_quotas(self, obj):
        return ",".join([f"{quota}" for quota in obj.quotas.all()])

    list_display: List[str] = ["id", "name", "zone", "root_path", "list_quotas"]
    readonly_fields: List[str] = ["deleted_at", "created_at", "updated_at"]
    inlines = [QuotaInLine]

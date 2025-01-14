from django.contrib import admin
from typing import List
from .models import Class, Quota
from apps.data.models import Dataset


class DatasetInLine(admin.TabularInline):
    model = Dataset
    extra = 0


class QuotaInLine(admin.TabularInline):
    model = Quota
    extra = 0


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
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
    readonly_fields = ["deleted_at", "created_at", "updated_at"]


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def list_quotas(self, obj):
        return ",".join([f"{quota}" for quota in obj.quotas.all()])

    list_display: List[str] = ["id", "name", "zone", "root_path", "list_quotas"]
    readonly_fields = ["deleted_at", "created_at", "updated_at"]
    inlines = [QuotaInLine]

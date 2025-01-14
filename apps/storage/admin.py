from django.contrib import admin
from typing import List
from .models import Class, Quota
from apps.data.models import Dataset


class DatasetInLine(admin.TabularInline):
    model = Dataset
    extra = 0


admin.site.register([Class])


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

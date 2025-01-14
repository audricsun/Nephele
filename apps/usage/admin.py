from django.contrib import admin
from .models import ClusterUsage, StorageUsage


admin.site.register(
    (
        ClusterUsage,
        StorageUsage,
    )
)

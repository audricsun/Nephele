from django.contrib import admin
from .models import ClusterUsage, StorageUsage, ClusterQuota, StorageQuota


admin.site.register(
    (
        ClusterUsage,
        StorageUsage,
        ClusterQuota,
        StorageQuota,
    )
)

from django.contrib import admin
from .models import ClusterResourceUsage, StorageUsage


admin.site.register(
    (
        ClusterResourceUsage,
        StorageUsage,
    )
)

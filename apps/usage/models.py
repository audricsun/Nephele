from django.db import models
from nephele.models import Model
from apps.project.models import Project


class ClusterUsage(Model):
    cpu_requested = models.IntegerField(default=0)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="cluster_usage"
    )


class StorageUsage(Model):
    storage_used = models.IntegerField(default=0)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="storage_usage"
    )

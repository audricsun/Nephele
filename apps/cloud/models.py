from django.db import models
from nephele.models import Model
from apps.project.models import Project


class Zone(Model):
    zone_id = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=False, blank=False, default="no description")

    def __str__(self):
        return f"{self.zone_id}"


class MembershipRole(models.TextChoices):
    k8s: tuple[str, str] = "k8s", "Kubernetes"


class ClusterProvider(Model):
    zone = models.OneToOneField(Zone, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.TextField(null=False, blank=False, default="no description")
    provider_type = models.CharField(
        max_length=64,
        unique=True,
        choices=MembershipRole.choices,
        default=MembershipRole.k8s,
    )
    cluster_endpoint = models.CharField(max_length=255, null=False, blank=False)
    cluster_auth = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.id}::{self.name}"


class ClusterCapacity(Model):
    zone = models.OneToOneField(Zone, on_delete=models.CASCADE, related_name="capacity")
    cluster_cpu_capacity = models.IntegerField(default=0)
    cluster_gpu_capacity = models.IntegerField(default=0)
    cluster_mem_capacity = models.IntegerField(default=0)

    def __str__(self):
        return f"cpu:{self.cluster_cpu_capacity} gpu:{self.cluster_gpu_capacity} mem:{self.cluster_mem_capacity}"


class Quota(Model):
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resource_quota",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="resource_quota",
        null=False,
        blank=False,
    )
    quota_cpu = models.IntegerField(default=0)
    quota_gpu = models.IntegerField(default=0)
    quota_mem = models.IntegerField(default=0)

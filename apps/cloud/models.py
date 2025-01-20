from django.db import models
from django.db.models import Q
from apps.project.models import Project
from nephele.models import Model
from django.core.exceptions import ValidationError


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "zone",
                    "project",
                ],
                condition=Q(deleted_at__isnull=True),
                name="unique_if_not_deleted",
            )
        ]

    def clean(self):
        if (
            self.__class__._default_manager.filter(zone=self.zone, project=self.project)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError("Quota for this project already exists")

    quota_cpu = models.IntegerField(default=0)
    quota_gpu = models.IntegerField(default=0)
    quota_mem = models.IntegerField(default=0)


class TaskQueue(Model):
    quota = models.ForeignKey(
        Quota,
        on_delete=models.CASCADE,
        related_name="queues",
        null=False,
        blank=False,
        db_comment="The quota that this queue belongs to",
    )


class ReservePlan(Model):
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name="reserve_plan"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reserve_plan"
    )
    reserve_cpu = models.IntegerField(default=0)
    reserve_gpu = models.IntegerField(default=0)
    reserve_mem = models.IntegerField(default=0)
    reserve_start = models.DateTimeField()
    reserve_end = models.DateTimeField()
    reserve_status = models.BooleanField(default=False)
    reserve_reason = models.TextField(null=False, blank=False, default="no reason")

    def __str__(self):
        return f"{self.project}::{self.reserve_cpu}::{self.reserve_gpu}::{self.reserve_mem}::{self.reserve_start}::{self.reserve_end}"


class Node(Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="nodes")
    cluster_provider = models.ForeignKey(
        ClusterProvider, on_delete=models.CASCADE, related_name="nodes"
    )
    node_name = models.CharField(max_length=64, unique=False, null=False, blank=False)
    node_ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    node_ib_ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    node_external_ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    node_status = models.BooleanField(default=False)
    node_cpu = models.IntegerField(default=0)
    node_gpu = models.IntegerField(default=0)
    node_mem = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.node_name}::{self.node_ip}"

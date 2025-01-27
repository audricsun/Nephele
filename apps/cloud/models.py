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


class ComputeQuota(Model):
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
        verbose_name = "ComputeQuota"
        verbose_name_plural = "ComputeQuotas"

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
    name = models.CharField(
        max_length=64, unique=True, null=False, blank=False, default="default"
    )
    quota = models.ForeignKey(
        ComputeQuota,
        on_delete=models.CASCADE,
        related_name="queues",
        null=False,
        blank=False,
        db_comment="The quota that this queue belongs to",
    )
    cpu_capacity = models.IntegerField(default=0)
    mem_capacity = models.IntegerField(default=0)
    gpu_capacity = models.IntegerField(default=0)
    queue_selector = models.JSONField(default=dict, null=True, blank=True)


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

    class Meta:
        verbose_name = "ReservePlan"
        verbose_name_plural = "ReservePlans"


class Node(Model):
    """
    Represents a node in the cloud infrastructure.

    Attributes:
        zone (ForeignKey): The zone to which the node belongs.
        node_name (CharField): The name of the node.
        node_ip (GenericIPAddressField): The IP address of the node.
        node_ib_ip (GenericIPAddressField): The InfiniBand IP address of the node.
        node_external_ip (GenericIPAddressField): The external IP address of the node.
        node_status (BooleanField): The status of the node (active/inactive).
        node_cpu (IntegerField): The number of CPUs in the node.
        node_gpu (IntegerField): The number of GPUs in the node.
        node_mem (IntegerField): The amount of memory in the node.

    Methods:
        __str__(): Returns a string representation of the node.
    """

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="nodes")
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


class ZoneCapacityStatic(Model):
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name="capacity_static"
    )
    audited_at = models.DateTimeField(auto_now=True)
    cpu_capacity = models.IntegerField(default=0)
    gpu_capacity = models.IntegerField(default=0)
    mem_capacity = models.IntegerField(default=0)

    def __str__(self):
        return (
            f"cpu:{self.cpu_capacity} gpu:{self.gpu_capacity} mem:{self.mem_capacity}"
        )

    class Meta:
        verbose_name = "Static"
        verbose_name_plural = "Statics"

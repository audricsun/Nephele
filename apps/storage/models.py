from django.db import models
from nephele.models import Model
from apps.cloud.models import Zone
from apps.project.models import Project
from django.core.exceptions import ValidationError


def validate_storage_class_host_path_root(value: str):
    if not value.startswith("/"):
        raise ValidationError("must start with slash /")
    if value.endswith("/"):
        raise ValidationError("should not end with trailing slash /")


# Create your models here.
class Class(Model):
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name="class_in_zone"
    )
    root_path = models.CharField(
        max_length=255, validators=[validate_storage_class_host_path_root]
    )

    def __str__(self) -> str:
        return f"Storage{self.name}@{self.zone.zone_id}"


class Quota(Model):
    owner = models.CharField(max_length=255, null=True, blank=True)
    limit = models.IntegerField(default=10)
    reserve = models.IntegerField(default=10)
    provider = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=False, blank=False, related_name="quotas"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True, related_name="quotas"
    )

    class Meta:
        unique_together: tuple[str] = (
            "provider",
            "project",
        )

    def quota_root(self) -> str:
        return f"{self.provider.root_path}/{self.project.name}-{self.id}"

    def used(self) -> int:
        return sum([dataset.used_size for dataset in self.datasets.all()])

    def available(self) -> int:
        return self.limit - self.used()

    def __str__(self):
        return f"Quota::{self.project.name}::{self.used()}/{self.limit}[{self.provider}]"

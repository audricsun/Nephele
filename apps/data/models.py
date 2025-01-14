from django.db import models
from nephele.models import Model
from itertools import chain
from apps.cloud.models import Zone
from apps.storage.models import Quota
from django.db.models.functions import Concat,Cast


class Layout(Model):
    display_name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.display_name} @{str(self.zone)}"

    def list_parent_mounts(self):
        if not self.parent:
            return []
        return chain(self.parent.list_parent_mounts(), self.parent.mounts.all())

    def list_mounts(self):
        if self.parent:
            parent_mounts = self.parent.list_mounts()

            return chain(parent_mounts, self.mounts.all())

        else:
            return self.mounts.all()


class Dataset(Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    display_name = models.CharField(max_length=255)
    default_mount = models.CharField(max_length=255)
    path = models.GeneratedField(
        expression=Concat(
            "name", models.Value("-"), Cast("id", models.CharField())
        ),
        output_field=models.CharField(max_length=100),
        db_persist=True,
    )
    quota = models.ForeignKey(
        Quota,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="datasets",
    )
    limit_size = models.IntegerField(default=0, null=False, blank=False)
    used_size = models.IntegerField(default=0, null=False, blank=False)
    access_level = models.IntegerField(default=0)

    def storage_path(self):
        return f"{self.quota.quota_root()}/{self.path}"

    def __str__(self) -> str:
        return f"{self.storage_path()} [{str(self.quota)}]"


class Mount(Model):
    layout = models.ForeignKey(
        Layout,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="mounts",
    )
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="mounts",
    )
    mount_path = models.CharField(max_length=255, null=True, blank=True)
    readonly = models.BooleanField(default=False)

    def mount(self):
        return self.mount_path or self.dataset.default_mount

    def __str__(self) -> str:
        return f"{self.dataset.storage_path()}:{self.mount()}"

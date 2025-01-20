from django.db import models
from nephele.models import Model
from apps.project.models import Project


class WorkloadType(Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    template_file = models.CharField(max_length=100, null=False, blank=False)


class Template(Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        db_comment="Description of the task template", null=True, blank=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        db_comment="All task template should belong to a project",
    )
    workload_type = models.ForeignKey(
        WorkloadType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="templates",
        db_comment="All task template should against one workload type",
    )
    entrypoint = models.CharField(max_length=100, null=True, blank=True)
    cmd = models.JSONField(default=dict)
    env_vars = models.JSONField(default=dict)
    selectors = models.JSONField(default=dict)

    cpu_limit = models.IntegerField(default=1)
    cpu_request = models.IntegerField(default=1)

    mem_limit = models.IntegerField(default=1)
    mem_request = models.IntegerField(default=1)

    storage_limit = models.IntegerField(default=1)
    storage_request = models.IntegerField(default=1)

    gpu_limit = models.IntegerField(default=0)
    gpu_model = models.CharField(max_length=100, null=True, blank=True)

    node_requested = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name}"


class Spec(Model):
    description = models.TextField(
        default="no desc at the point",
        db_comment="Description of the task template",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        null=True,
        db_comment="All task spec should against one task template",
    )

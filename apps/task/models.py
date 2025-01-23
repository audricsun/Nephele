from django.db import models
from nephele.models import Model
from apps.project.models import Project
from django.template.loader import render_to_string


class WorkloadType(Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    template_file = models.CharField(max_length=100, null=False, blank=False)


class Template(Model):
    """some template for task"""

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
    work_dir = models.CharField(max_length=100, null=True, blank=True)

    def _default_cmd():
        return ["echo", "hello-world!"]

    cmd = models.JSONField(default=_default_cmd)
    env_vars = models.JSONField(default=dict, null=True, blank=True)
    selectors = models.JSONField(default=dict, null=True, blank=True)
    artifacts = models.JSONField(default=list, null=True, blank=True)

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

    def render(self):
        return render_to_string(
            self.workload_type.template_file,
            {
                "name": self.name,
                "description": self.description,
                "entrypoint": self.entrypoint,
                "cmd": self.cmd,
                "env_vars": self.env_vars,
                "selectors": self.selectors,
                "cpu_limit": self.cpu_limit,
                "cpu_request": self.cpu_request,
                "mem_limit": self.mem_limit,
                "mem_request": self.mem_request,
                "storage_limit": self.storage_limit,
                "storage_request": self.storage_request,
                "gpu_limit": self.gpu_limit,
                "gpu_model": self.gpu_model,
                "node_requested": self.node_requested,
            },
        )


class Spec(Model):
    note = models.TextField(
        default="no desc at the point",
        db_comment="Description of the task template",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        null=True,
        db_comment="All task spec should against one task template",
    )


class BatchTask(Model):
    display_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    spec = models.ForeignKey(
        Spec,
        on_delete=models.CASCADE,
        null=False,
        db_comment="All task should against one task spec",
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        null=False,
    )

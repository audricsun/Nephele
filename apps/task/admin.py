from django.contrib import admin
from .models import Template, Spec, WorkloadType, BatchTask

admin.site.register(
    [
        WorkloadType,
        Template,
        Spec,
        BatchTask,
    ]
)

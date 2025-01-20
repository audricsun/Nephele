from django.contrib import admin
from .models import Template, Spec, WorkloadType

admin.site.register(
    [
        WorkloadType,
        Template,
        Spec,
    ]
)

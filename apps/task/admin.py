from django.contrib import admin
from .models import Template, Spec, WorkloadType, BatchTask
from unfold.admin import ModelAdmin
from nephele.models import ModelAdminUpdateBy


@admin.register(WorkloadType)
class WorkloadTypeAdmin(ModelAdmin):
    pass


@admin.register(Template)
class TemplateAdmin(ModelAdminUpdateBy):
    list_display = ("name", "workload_type", "entrypoint", "created_by", "updated_by")
    readonly_fields = ("created_by", "updated_by")


@admin.register(Spec)
class SpecAdmin(ModelAdminUpdateBy):
    pass


@admin.register(BatchTask)
class BatchTaskAdmin(ModelAdminUpdateBy):
    pass

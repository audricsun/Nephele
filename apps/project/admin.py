from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, Membership, ProjectSettings
from apps.storage.models import Quota as sQuota
from apps.cloud.models import Quota as cQuota


class ProjectSettingsInline(admin.StackedInline):
    model = ProjectSettings
    can_delete = False
    verbose_name_plural = "settings"


class ProjectMemberInline(admin.TabularInline):
    model = Membership
    extra = 0


class StorageQuotaInline(admin.TabularInline):
    model = sQuota
    extra = 0


class ComputingQuotaInline(admin.TabularInline):
    model = cQuota
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def direct_members(self, obj):
        # return ",".join([str(m) for m in obj.direct_membership()])
        return mark_safe(
            f"<ul>{''.join([f'<li>{str(m)}</li>' for m in obj.direct_membership()])}</ul>"
        )

    def parent_members(self, obj) -> str:
        # return ",".join([str(m) for m in obj.parent_memberships()])
        return mark_safe(
            f"<ul>{''.join([f'<li>{str(m)}</li>' for m in obj.parent_memberships()])}</ul>"
        )

    def member_max_roles(self, obj) -> str:
        return [
            f"{mr.get('user_name')}<{mr.get('user_id')}>[role={mr.get('max_role')}]"
            for mr in obj.all_membership_with_max_role()
        ]

    list_display: tuple[str] = (
        "id",
        "name",
        "display_name",
        "is_active",
        "slug",
        "nested_depth",
        "description",
        "parent",
        "member_max_roles",
        "direct_members",
        "parent_members",
        "updated_at",
        "created_at",
    )
    member_max_roles.short_description = "Membership(Max Role)"
    inlines: tuple[str] = (
        ProjectMemberInline,
        ProjectSettingsInline,
        ComputingQuotaInline,
        StorageQuotaInline,
    )
    list_filter: tuple[str] = (
        "is_active",
        "created_at",
        "updated_at",
        "private",
    )
    save_on_top = True
    ordering: tuple[str] = (
        "updated_at",
        "created_at",
    )
    readonly_fields: tuple[str] = (
        "created_at",
        "updated_at",
        "deleted_at",
        "parent_members",
        "member_max_roles",
    )
    list_editable = ("display_name",)
    search_fields = [
        "name",
    ]

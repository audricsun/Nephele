from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Project, Membership, ProjectSettings
from apps.storage.models import StorageCapacity as sQuota
from apps.cloud.models import ComputeQuota as cQuota
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline, TabularInline


class ProjectSettingsInline(StackedInline):
    model = ProjectSettings
    can_delete = False
    verbose_name_plural = "settings"
    tab = True


class ProjectMemberInline(TabularInline):
    model = Membership
    extra = 0
    # tab = True


class StorageQuotaInline(TabularInline):
    model = sQuota
    extra = 0
    tab = True


class ComputingQuotaInline(TabularInline):
    model = cQuota
    extra = 0
    tab = True


def mark_list(input_list: list[str]) -> str:
    return mark_safe(f"<ul>{''.join([f'<li>{str(m)}</li>' for m in input_list])}</ul>")


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    """hide some fields in admin"""

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
        return mark_list(
            [
                f"{mr.get('user_name')}<{mr.get('user_id')}>[role={mr.get('max_role')}]"
                for mr in obj.all_membership_with_max_role()
            ]
        )

    list_display: tuple[str] = (
        "slug",
        # "id",
        "name",
        # "display_name",
        "is_active",
        # "nested_depth",
        # "description",
        "parent",
        "member_max_roles",
        # "direct_members",
        # "parent_members",
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
    search_fields = [
        "name",
    ]

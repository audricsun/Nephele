from django.contrib import admin
from .models import Project, Membership

# Register your models here.


class ProjectMemberInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def direct_members(self, obj):
        return ",".join([str(m) for m in obj.direct_membership()])

    def parent_members(self, obj) -> str:
        return ",".join([str(m) for m in obj.parent_memberships()])

    def member_max_roles(self, obj) -> str:
        return [
            f"{mr.get("user_name")}<{mr.get("user_id")}>[role={mr.get("max_role")}]"
            for mr in obj.all_membership_with_max_role()
        ]

    list_display: tuple[str] = (
        "id",
        "name",
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
    inlines: tuple[str] = (ProjectMemberInline,)
    list_filter: tuple[str] = (
        "is_active",
        "created_at",
        "updated_at",
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
    list_editable = ("name",)
    search_fields = [
        "name",
    ]

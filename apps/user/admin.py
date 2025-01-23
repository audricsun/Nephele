from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .models import UserProjectNamespace, UserSettings, UserProfile


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProjectInline(admin.StackedInline):
    model = UserProjectNamespace
    can_delete = False
    verbose_name_plural = "private_projects"


class SettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    verbose_name_plural = "settings"


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserProjectInline, ProfileInline, SettingsInline]
    list_display = BaseUserAdmin.list_display + ("personal_project",)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

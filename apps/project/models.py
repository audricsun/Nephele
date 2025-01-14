from django.contrib.auth.models import User
from django.db import models
from nephele.models import Model
from typing import Any, Dict, List
from django.db.models import Max


# Define the Project model
class Project(Model):
    name = models.CharField(max_length=255)  # Project name
    description = models.TextField(null=True, blank=True)  # Project description
    is_active = models.BooleanField(default=True)  # Project active status
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # Parent project (self-referential foreign key)
    members = models.ManyToManyField(
        User,
        through="Membership",
        related_name="projects",
    )  # Many-to-many relationship with User through Membership

    # Generate a slug for the project
    def slug(self) -> str:
        if not self.parent:
            return f"/{self.name}"
        return self.parent.slug() + "/" + self.name

    # Calculate the nested depth of the project
    def nested_depth(self) -> str:
        if not self.parent:
            return 1
        return self.parent.nested_depth() + 1

    # String representation of the project
    def __str__(self) -> str:
        return self.name

    # Retrieve the members of the parent project
    def parent_members(self) -> models.QuerySet:
        if not self.parent:
            return User.objects.none()
        return self.parent.parent_members() | self.parent.members.all()

    # Retrieve all members of the project, including parent members
    def all_members(self) -> models.QuerySet:
        return self.parent_members() | self.members.all()

    def direct_membership(self) -> models.QuerySet:
        return self.members.through.objects.filter(project=self)

    # Retrieve the memberships of the parent project
    def parent_memberships(self) -> models.QuerySet:
        if self.parent is None:
            return self.members.through.objects.none()
        return self.parent.parent_memberships() | self.members.through.objects.filter(
            project=self.parent
        )

    # Retrieve all memberships of the project, including parent memberships
    def all_memberships(self) -> models.QuerySet:
        return (self.parent_memberships() | self.direct_membership()).annotate(
            user_name=models.F("user__username"),
            user_email=models.F("user__email"),
            user_role=models.F("role"),
            project_name=models.F("project__name"),
        )

    # Retrieve members with their maximum role in the project
    def all_membership_with_max_role(self) -> List[Dict[str, Any]]:
        return (
            self.all_memberships()
            .values("user_name", "user_email", "user_id")
            .annotate(max_role=Max("user_role"))
        )


# Define the MembershipRole choices
class MembershipRole(models.IntegerChoices):
    BAN: tuple[int, str] = -1, "Banned"
    GUEST: tuple[int, str] = 10, "Guest"
    READER: tuple[int, str] = 20, "Reader"
    WRITER: tuple[int, str] = 100, "Writer"
    ADMIN: tuple[int, str] = 1000, "Admin"


# Define the Membership model
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User in the membership
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE
    )  # Project in the membership
    date_joined = models.DateField(auto_now=True)  # Date the user joined the project
    role = models.IntegerField(
        choices=MembershipRole.choices,
        default=MembershipRole.GUEST,
        verbose_name="role",
    )  # Role of the user in the project
    invite_reason = models.CharField(
        max_length=64, default="n/a"
    )  # Reason for the invitation

    # String representation of the membership
    def __str__(self):
        return f"{self.project}::{self.user}::{self.get_role_display()}"

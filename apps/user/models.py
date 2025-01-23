from django.contrib.auth.models import User
from django.db import models
from nephele.models import Model
from django_lifecycle import hook, BEFORE_CREATE
from loguru import logger


class UserProjectNamespace(Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="personal_project"
    )
    active = models.BooleanField(default=False)
    note = models.CharField(max_length=100, null=True, blank=True)

    @hook(BEFORE_CREATE)
    def on_before_create(self):
        logger.debug("before_create")

    def __str__(self):
        return f"{self.user}: {self.active}"


class UserSettings(Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="settings",
    )
    notification_level = models.IntegerField(default=0)


class UserProfile(Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    theme = models.CharField(max_length=100)
    locale = models.CharField(max_length=100)

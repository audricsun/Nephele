from django.contrib.auth.models import User
from django.db import models
from nephele.models import Model


class Employee(Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department


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

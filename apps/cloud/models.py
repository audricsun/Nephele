from django.db import models
from nephele.models import Model


class Zone(Model):
    zone_id = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=False, blank=False, default="no description")

    def __str__(self):
        return f"{self.display_name}({self.zone_id})"

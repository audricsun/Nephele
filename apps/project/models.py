from django.db import models
from nephele.models import Model


class Project(Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # owner = models.ForeignKey("User", on_delete=models.CASCADE)
    # members = models.ManyToManyField("User", related_name="projects")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

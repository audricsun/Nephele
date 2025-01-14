from django.db import models
from nephele.models import Model


class Template(Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return self.name

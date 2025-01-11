from django.db import models
import uuid


class Timestampable(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SoftDeletes(models.Model):
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class UuidPk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Model(UuidPk, Timestampable, SoftDeletes, models.Model):
    class Meta:
        abstract = True

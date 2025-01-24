import uuid

from django.db import models, router
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin
from . import signals
from .managers import SoftDeleteManager
from django.contrib.auth.models import User


class Timestampable(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SoftDeletes(models.Model):
    # inspired by https://github.com/xgeekshq/django-timestampable/blob/main/timestamps/models.py
    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=False, verbose_name=_("deleted_at")
    )

    objects = SoftDeleteManager()
    objects_deleted = SoftDeleteManager(only_deleted=True)
    objects_with_deleted = SoftDeleteManager(with_deleted=True)

    class Meta:
        abstract = True

    def delete(
        self, using=None, keep_parents: bool = False, hard: bool = False
    ) -> None:
        if hard:
            return super().delete(using, keep_parents)

        using = using or router.db_for_write(self.__class__, instance=self)

        signals.pre_soft_delete.send(sender=self.__class__, instance=self, using=using)

        self.deleted_at: timezone.datetime = timezone.now()
        self.save()

        signals.post_soft_delete.send(sender=self.__class__, instance=self, using=using)

    def soft_delete(self) -> None:
        self.delete(hard=False)

    def hard_delete(self, using=None, keep_parents: bool = False):
        return self.delete(using, keep_parents, hard=True)

    def restore(self) -> None:
        signals.pre_restore.send(sender=self.__class__, instance=self)

        self.deleted_at = None
        self.save()

        signals.post_restore.send(sender=self.__class__, instance=self)


class UuidPk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TrackUserOperation(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(model_name)s_%(class)s_created_by",
        null=True,
        blank=True,
    )
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(model_name)s_%(class)s_deleted_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Model(
    UuidPk,
    Timestampable,
    SoftDeletes,
    # TrackUserOperation, # TODO: add user operation track to base model
    LifecycleModelMixin,
    models.Model,
):
    class Meta:
        abstract = True

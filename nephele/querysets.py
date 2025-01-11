from django.db.models import QuerySet
from django.utils import timezone


class SoftDeleteQuerySet(QuerySet):
    def only_deleted(self):
        return self.filter(deleted_at__isnull=False)

    def without_deleted(self):
        return self.filter(deleted_at__isnull=True)

    #  bulk delete
    def delete(self, hard: bool = False):
        if hard:
            return super().delete()

        return super().update(deleted_at=timezone.now())

    #  bulk restore (new feature!)
    def restore(self):
        return super().update(deleted_at=None)
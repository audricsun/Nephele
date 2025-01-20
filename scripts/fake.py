import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nephele.settings")

import django

django.setup()

if __name__ == "__main__":
    # Project should be provisioned first
    # It's a global model, and other models depend on it
    from apps.project.models import Project

    fake_proj_p0, is_new = Project.objects.update_or_create(
        name="fake-project-01", description="fake project 01"
    )
    fake_proj_p1, is_new = Project.objects.update_or_create(
        name="fake-project-02", description="fake project 02", parent=fake_proj_p0
    )

    # Zone is also a global model, all actual resources should belong to a zone
    from apps.cloud.models import Zone

    fake_zone, is_new = Zone.objects.update_or_create(zone_id="fake-01")
    print(fake_zone)

    # Storage Class is a zoned model, it should belong to a zone
    from apps.storage.models import Class

    default_storage_class, is_new = Class.objects.update_or_create(
        name="t0", zone=fake_zone, root_path="/dev/tier-0"
    )

    # some test members
    from django.contrib.auth.models import User

    User.objects.bulk_create(
        [
            User(
                username=f"test-user-{i:02d}",
                email=f"test-user-{i:02d}@example.com",
                first_name="test",
                last_name=f"user-{i:02d}",
            )
            for i in range(10)
        ],
        update_conflicts=True,
        unique_fields=["username"],
        update_fields=["email"],
    )

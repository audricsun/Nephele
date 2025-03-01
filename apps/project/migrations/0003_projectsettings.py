# Generated by Django 5.1.5 on 2025-01-20 09:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_project_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSettings',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

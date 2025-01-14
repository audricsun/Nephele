# Generated by Django 5.1.4 on 2025-01-14 08:39

import apps.storage.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cloud', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('root_path', models.CharField(max_length=255, validators=[apps.storage.models.validate_storage_class_host_path_root])),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_in_zone', to='cloud.zone')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.CharField(blank=True, max_length=255, null=True)),
                ('limit', models.IntegerField(default=10)),
                ('reserve', models.IntegerField(default=10)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotas', to='project.project')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotas', to='storage.class')),
            ],
            options={
                'unique_together': {('provider', 'project')},
            },
        ),
    ]

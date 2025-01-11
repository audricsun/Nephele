# Generated by Django 5.1.4 on 2025-01-11 03:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('zone_id', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(default='no description')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

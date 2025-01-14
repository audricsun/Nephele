# Generated by Django 5.1.4 on 2025-01-14 05:07

import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('display_name', models.CharField(max_length=255)),
                ('default_mount', models.CharField(max_length=255)),
                ('path', models.GeneratedField(db_persist=True, expression=django.db.models.functions.text.Concat('name', models.Value('-'), django.db.models.functions.comparison.Cast('id', models.CharField())), output_field=models.CharField(max_length=100))),
                ('limit_size', models.IntegerField(default=0)),
                ('used_size', models.IntegerField(default=0)),
                ('access_level', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mount',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mount_path', models.CharField(blank=True, max_length=255, null=True)),
                ('readonly', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

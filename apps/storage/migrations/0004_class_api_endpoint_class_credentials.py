# Generated by Django 5.1.5 on 2025-01-21 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_class_capacity_class_capacity_inodes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='api_endpoint',
            field=models.CharField(default='http://example.com', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='credentials',
            field=models.TextField(default='dummy'),
            preserve_default=False,
        ),
    ]

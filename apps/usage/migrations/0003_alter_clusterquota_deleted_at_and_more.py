# Generated by Django 5.1.5 on 2025-01-20 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0002_clusterquota_storagequota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clusterquota',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at'),
        ),
        migrations.AlterField(
            model_name='clusterusage',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at'),
        ),
        migrations.AlterField(
            model_name='storagequota',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at'),
        ),
        migrations.AlterField(
            model_name='storageusage',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-27 08:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_layoutv2'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Layoutv2',
            new_name='LayoutWithTN',
        ),
        migrations.AlterModelOptions(
            name='layoutwithtn',
            options={'verbose_name': 'Layout-v2', 'verbose_name_plural': 'Layouts-v2'},
        ),
    ]

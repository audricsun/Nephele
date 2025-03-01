# Generated by Django 5.1.5 on 2025-01-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_projectsettings_access_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='display_name',
            field=models.CharField(default='no', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(editable=False, max_length=255),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-21 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0004_taskqueue_cpu_capacity_taskqueue_gpu_capacity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskqueue',
            name='name',
            field=models.CharField(default='default', max_length=64, unique=True),
        ),
    ]

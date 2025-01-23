# Generated by Django 5.1.5 on 2025-01-20 10:25

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_remove_template_css_remove_template_html_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(db_comment='Description of the task template', default='no desc at the point')),
                ('template', models.ForeignKey(db_comment='All task spec should against one task template', null=True, on_delete=django.db.models.deletion.CASCADE, to='task.template')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

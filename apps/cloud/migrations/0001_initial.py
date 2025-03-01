# Generated by Django 5.1.4 on 2025-01-14 08:39

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterProvider',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(default='no description')),
                ('provider_type', models.CharField(choices=[('k8s', 'Kubernetes')], default='k8s', max_length=64, unique=True)),
                ('cluster_endpoint', models.CharField(max_length=255)),
                ('cluster_auth', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
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
        migrations.CreateModel(
            name='ReservePlan',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reserve_cpu', models.IntegerField(default=0)),
                ('reserve_gpu', models.IntegerField(default=0)),
                ('reserve_mem', models.IntegerField(default=0)),
                ('reserve_start', models.DateTimeField()),
                ('reserve_end', models.DateTimeField()),
                ('reserve_status', models.BooleanField(default=False)),
                ('reserve_reason', models.TextField(default='no reason')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_plan', to='project.project')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserve_plan', to='cloud.zone')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('node_name', models.CharField(max_length=64)),
                ('node_ip', models.GenericIPAddressField()),
                ('node_ib_ip', models.GenericIPAddressField()),
                ('node_external_ip', models.GenericIPAddressField()),
                ('node_status', models.BooleanField(default=False)),
                ('node_cpu', models.IntegerField(default=0)),
                ('node_gpu', models.IntegerField(default=0)),
                ('node_mem', models.IntegerField(default=0)),
                ('cluster_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='cloud.clusterprovider')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='cloud.zone')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='clusterprovider',
            name='zone',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cloud.zone'),
        ),
        migrations.CreateModel(
            name='ClusterCapacity',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cluster_cpu_capacity', models.IntegerField(default=0)),
                ('cluster_gpu_capacity', models.IntegerField(default=0)),
                ('cluster_mem_capacity', models.IntegerField(default=0)),
                ('zone', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='capacity', to='cloud.zone')),
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
                ('quota_cpu', models.IntegerField(default=0)),
                ('quota_gpu', models.IntegerField(default=0)),
                ('quota_mem', models.IntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_quota', to='project.project')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource_quota', to='cloud.zone')),
            ],
            options={
                'constraints': [models.UniqueConstraint(condition=models.Q(('deleted_at__isnull', True)), fields=('zone', 'project'), name='unique_if_not_deleted')],
            },
        ),
    ]

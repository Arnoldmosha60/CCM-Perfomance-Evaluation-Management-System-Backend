# Generated by Django 5.0.6 on 2024-08-03 03:06

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('indicator', models.CharField()),
                ('indicator_code', models.CharField(max_length=5, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('indicator_value', models.FloatField()),
                ('achievement_percentage', models.FloatField(default=0.0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'indicator',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('activity', models.CharField()),
                ('activity_code', models.CharField(max_length=5, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('activity_value', models.FloatField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccm.indicator')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('objective', models.CharField()),
                ('objective_code', models.CharField(max_length=5, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'objective',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('target', models.CharField()),
                ('target_code', models.CharField(max_length=5, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccm.objective')),
            ],
            options={
                'db_table': 'target',
            },
        ),
        migrations.AddField(
            model_name='indicator',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccm.target'),
        ),
        migrations.CreateModel(
            name='WilayaRepresentative',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('wilaya', models.CharField(max_length=50)),
                ('mkoa', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('wilaya_code', models.CharField(max_length=5, unique=True)),
                ('representative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'representative',
            },
        ),
        migrations.AddField(
            model_name='objective',
            name='representative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccm.wilayarepresentative'),
        ),
    ]

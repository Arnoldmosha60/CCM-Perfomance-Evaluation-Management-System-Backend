# Generated by Django 5.0.6 on 2024-06-28 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ccm', '0002_indicator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicator',
            old_name='Target',
            new_name='target',
        ),
    ]

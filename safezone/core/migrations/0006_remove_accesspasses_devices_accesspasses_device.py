# Generated by Django 5.2.1 on 2025-05-22 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_accesspasses_qr_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accesspasses',
            name='devices',
        ),
        migrations.AddField(
            model_name='accesspasses',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.devices'),
        ),
    ]

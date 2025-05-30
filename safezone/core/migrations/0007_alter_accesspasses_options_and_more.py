# Generated by Django 5.2.1 on 2025-05-22 15:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_accesspasses_devices_accesspasses_device'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesspasses',
            options={'verbose_name': 'Пропуск', 'verbose_name_plural': 'Пропуска'},
        ),
        migrations.AlterField(
            model_name='accesslogs',
            name='access_pass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.accesspasses', verbose_name='Пропуск'),
        ),
        migrations.AlterField(
            model_name='accesslogs',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='accesslogs',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.devices', verbose_name='Турникет'),
        ),
        migrations.AlterField(
            model_name='accesslogs',
            name='timestamp',
            field=models.DateTimeField(verbose_name='Время прохода'),
        ),
        migrations.AlterField(
            model_name='accesslogs',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.devices', verbose_name='Турникет'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.facilities', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/', verbose_name='QR-код'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='valid_from',
            field=models.DateTimeField(verbose_name='Действует с'),
        ),
        migrations.AlterField(
            model_name='accesspasses',
            name='valid_to',
            field=models.DateTimeField(verbose_name='Действует по'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='api_token',
            field=models.CharField(max_length=255, verbose_name='API токен'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='api_url',
            field=models.CharField(max_length=255, verbose_name='API URL'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.facilities', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='admin',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'admin'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Администратор'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='facilities',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
    ]

from django.db import models
from django.conf import settings


class Facilities(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              limit_choices_to={'role': 'admin'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Devices(models.Model):
    title = models.CharField(max_length=255)
    facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    guard = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                              limit_choices_to={'role': 'guard'})
    api_url = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Турникет'
        verbose_name_plural = 'Турникеты'


class AccessPasses(models.Model):
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='pass_photos/', null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    note = models.TextField(null=True, blank=True)
    facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Devices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуски'


class AccessLogs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Devices, on_delete=models.SET_NULL, null=True)
    access_pass = models.ForeignKey(AccessPasses, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Лог пропуска'
        verbose_name_plural = 'Логи пропусков'

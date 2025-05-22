from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Суперадмин'
        ADMIN = 'admin', 'Администратор объекта'
        TECHNICIAN = 'technician', 'Техник'

    role = models.CharField(max_length=20, choices=Role.choices)
    facility = models.ForeignKey('core.Facilities', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Invite(models.Model):
    email = models.EmailField('Email', unique=True)
    token = models.CharField('Токен', max_length=64, unique=True)
    role = models.CharField('Роль', max_length=20, choices=User.Role.choices)
    facility = models.ForeignKey('core.Facilities', verbose_name='Объект', null=True, blank=True, on_delete=models.SET_NULL)
    used_at = models.DateTimeField('Использовано', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Приглашение на регистрацию'
        verbose_name_plural = 'Приглашения на регистрацию'

    def __str__(self):
        return f'{self.pk} : {self.email}'



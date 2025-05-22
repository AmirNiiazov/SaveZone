from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from safezone.settings import CRYPTO_KEY
from cryptography.fernet import Fernet


class Facilities(models.Model):
    title = models.CharField('Название', max_length=255)
    location = models.CharField('Адрес', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Администратор',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'admin'}
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return f'{self.pk} : {self.title}'


class Devices(models.Model):
    title = models.CharField('Название', max_length=255)
    facility = models.ForeignKey(Facilities, verbose_name='Объект', on_delete=models.CASCADE)
    is_active = models.BooleanField('Активен', default=True)
    description = models.TextField('Описание', null=True, blank=True)
    api_url = models.CharField('API URL', max_length=255)
    api_token = models.CharField('API токен', max_length=255)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Турникет'
        verbose_name_plural = 'Турникеты'

    def __str__(self):
        return f'{self.pk} : {self.title}'


class AccessPasses(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует по')
    note = models.TextField('Комментарий', null=True, blank=True)
    facility = models.ForeignKey(Facilities, verbose_name='Объект', on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, verbose_name='Турникет', on_delete=models.CASCADE, null=True, blank=True)
    qr_code = models.ImageField('QR-код', upload_to='qrcodes/', blank=True, null=True)
    qr_code_data = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуска'

    def generate_qr_code(self):
        if self.qr_code:
            return

        data = f'{self.full_name}|{self.valid_from.isoformat()}|{self.valid_to.isoformat()}|{self.pk}'
        fernet = Fernet(CRYPTO_KEY)
        encrypted = fernet.encrypt(data.encode())

        qr_img = qrcode.make(encrypted)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)

        file_name = f'qr_{self.pk}.png'
        print(encrypted.decode())
        self.qr_code_data = encrypted.decode()

        # Сохраняем изображение в поле, но не триггерим save() заново
        self.qr_code.save(file_name, File(buffer), save=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code', 'qr_code_data'])

    def __str__(self):
        return f"{self.full_name} ({self.valid_from:%d.%m.%Y} - {self.valid_to:%d.%m.%Y})"


class AccessLogs(models.Model):
    timestamp = models.DateTimeField('Время прохода')
    device = models.ForeignKey(Devices, verbose_name='Турникет', on_delete=models.SET_NULL, null=True)
    access_pass = models.ForeignKey(AccessPasses, verbose_name='Пропуск', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Лог пропуска'
        verbose_name_plural = 'Логи пропусков'

    def __str__(self):
        if self.access_pass and self.device:
            return f"{self.access_pass.full_name} через {self.device.title} — {self.timestamp:%d.%m.%Y %H:%M:%S}"
        return f"Проход от {self.timestamp}"

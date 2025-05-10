from django.contrib import admin
from . import models


admin.site.register(models.Facilities)

admin.site.register(models.Devices)

admin.site.register(models.AccessPasses)

admin.site.register(models.AccessLogs)

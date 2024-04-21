from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.WSTask)
admin.site.register(models.PTask)
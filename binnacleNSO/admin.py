from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Superuser)
admin.site.register(models.Subuser)
admin.site.register(models.Entry)
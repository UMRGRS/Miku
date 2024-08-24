from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = ((None, 
                  {'fields':('username', 'email', 'password')}), ('Permissions',{'fields':('is_staff', 'is_active', 'is_superuser')}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2',)}),)
    search_fields =('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
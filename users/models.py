from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise ValueError('Users must have a username')
        if email is None:
            raise ValueError('Users must have an email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        return user
        
    def create_standard_user(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_active, user.is_staff, user.is_superuser = True, True, True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # db_index is good for faster lookups in fields that are constantly being filter
    username = models.CharField(_('Username'), db_index=True, max_length=20, unique=True, blank=False, null=False)
    email = models.EmailField(_('Email'), blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

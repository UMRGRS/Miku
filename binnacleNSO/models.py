import os
from uuid import uuid4
import random as rnd

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)

# Create your models here.
class Superuser(models.Model):
    name = models.CharField(_('Super usuario'), unique=True, max_length=40, blank=False)
    streak = models.PositiveIntegerField(_('Racha'), default=0)
    numberOfEntries = models.PositiveIntegerField(_('Numero de entradas'), default=0)
    lastEntryDate = models.DateField(_('Ultima entrada'), default=None)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = '@' + self.name
        super(Superuser, self).save(*args, **kwargs)
        
    def addEntry(self):
        self.numberOfEntries = self.numberOfEntries + 1
        self.streak += 1
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Superuser')
        verbose_name_plural = _('Superusers')
    
class Subuser(models.Model):
    name = models.CharField(_('Sub usuario'), unique=True, max_length=40, blank=False)
    image = models.ImageField(_('Imagen'), upload_to=UploadToPathAndRename(os.path.join('media/usersPhotos')), default='media/usersPhotos/default.jpg')
    superuser = models.ForeignKey(('Superuser'), on_delete=models.CASCADE, related_name='superuser')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = '@' + self.name
        super(Subuser, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Subuser')
        verbose_name_plural = _('Subusers')
        
class Entry(models.Model):
    content = models.TextField(_('Contenido'), max_length=200, blank=False)
    stars = models.PositiveIntegerField(_('Estrellas'), default=1)
    shares = models.PositiveIntegerField(_('Retweets'), default=1)
    image = models.ImageField(_('Imagen'), upload_to=UploadToPathAndRename(os.path.join('media/entriesPhotos')), blank=True, null=True)
    day = models.PositiveIntegerField(_('Numero de entrada'), default=1)
    subuser = models.ForeignKey(('Subuser'), on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            modifier = self.subuser.superuser.streak*10
            self.stars = rnd.randint(10+modifier,20+modifier)
            self.shares = rnd.randint(6+int(modifier/2),12+int(modifier/2))
            self.day = self.subuser.superuser.numberOfEntries+1
            superuser = Superuser.objects.get(pk=self.subuser.superuser.pk)
            superuser.addEntry()
            superuser.save()
        super(Entry, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
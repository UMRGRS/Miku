import os
import cv2

from uuid import uuid4

from random import randint

from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

usersPhotosFolder = 'media/usersPhotos'
entriesPhotosFolder = 'media/entriesPhotos'

# Create your models here.
@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)

class Superuser(models.Model):
    name = models.CharField(_('Super usuario'), unique=True, max_length=40, blank=False)
    password = models.CharField(_('Contraseña'), max_length=50)
    streak = models.PositiveIntegerField(_('Racha'), default=0)
    numberOfEntries = models.PositiveIntegerField(_('Numero de entradas'), default=0)
    lastEntryDate = models.DateField(_('Ultima entrada'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = '@' + self.name
        super(Superuser, self).save(*args, **kwargs)
        
    def addEntry(self):
        self.numberOfEntries += 1
        self.streak += 1
        self.lastEntryDate = date.today()
    
    def resetStreak(self):
        if((date.today()-self.lastEntryDate).days > 1):
            self.streak = 0

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Superuser')
        verbose_name_plural = _('Superusers')
    
class Subuser(models.Model):
    name = models.CharField(_('Sub usuario'), unique=True, max_length=40, blank=False)
    image = ResizedImageField(_('Imagen'), size=[200,200], upload_to=UploadToPathAndRename(usersPhotosFolder), keep_meta=False, force_format='JPEG', default='media/usersPhotos/default.jpg')
    superuser = models.ForeignKey(('Superuser'), on_delete=models.CASCADE)
    
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
    image = models.ImageField(_('Imagen'), upload_to=UploadToPathAndRename(entriesPhotosFolder), blank=True, null=True)
    day = models.PositiveIntegerField(_('Numero de entrada'), default=1)
    superuser = models.ForeignKey(('Superuser'), on_delete=models.CASCADE)
    subuser = models.ForeignKey(('Subuser'), on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            modifier = self.subuser.superuser.streak*10
            self.stars = randint(10+modifier,20+modifier)
            self.shares = randint(6+int(modifier/2),12+int(modifier/2))
            self.day = self.subuser.superuser.numberOfEntries+1
            superuser = self.subuser.superuser
            superuser.addEntry()
            superuser.save()
        super(Entry, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

@receiver(post_save, sender=Entry)
def modifyEntryImage(sender, instance, created, **kwargs):
    if(created and instance.image.name != None):
        img = cv2.imread(instance.image.name)
        filename = instance.image.name.split('/')[-1]
        res = cv2.xphoto.oilPainting(img, 9, 2)
        cv2.imwrite(os.path.join(entriesPhotosFolder, filename), res)
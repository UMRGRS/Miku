import os
import cv2

# for unique ids in uploaded images
from uuid import uuid4

# To randomize stats in posts
from random import randint

from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

usersPhotosFolder = 'usersPhotos'
entriesPhotosFolder = 'entriesPhotos'

# Create your models here.
@deconstructible
# Rename image to unique id and return correct path
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class Profile(models.Model):
    name = models.CharField(_('Name'), unique=True, max_length=40, blank=False)
    # Streak is used to scale stars and retweets of entries
    streak = models.PositiveIntegerField(_('Streak'), default=0)
    # last entry date is used to reset streak
    lastEntryDate = models.DateField(_('Last entry date'), blank=True, null=True)
    owner = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    def addEntry(self):
        self.streak += 1
        self.lastEntryDate = date.today()

    def resetStreak(self):
        if ((date.today()-self.lastEntryDate).days > 1):
            self.streak = 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Alias(models.Model):
    name = models.CharField(_('Alias'), unique=True,max_length=40, blank=False)
    image = ResizedImageField(_('Image'), size=[200, 200], upload_to=UploadToPathAndRename(
        usersPhotosFolder), keep_meta=False, force_format='JPEG', default='media/usersPhotos/default.jpg')
    profile = models.ForeignKey(('Profile'), on_delete=models.CASCADE, related_name="alias")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Alias')
        verbose_name_plural = _('Aliases')


class Entry(models.Model):
    content = models.TextField(_('Content'), max_length=200, blank=False)
    stars = models.PositiveIntegerField(_('Stars'), default=1)
    shares = models.PositiveIntegerField(_('Retweets'), default=1)
    image = models.ImageField(_('Image'), upload_to=UploadToPathAndRename(entriesPhotosFolder), blank=True, null=True)
    entryDate = models.DateField(_('Entry date'), auto_now_add=True, null=False, blank=False)
    profile = models.ForeignKey(('Profile'), on_delete=models.CASCADE, related_name="entry")
    alias = models.ForeignKey(('Alias'), on_delete=models.CASCADE, related_name="entry")

    # Randomize entry's stats and save the entry
    def save(self, *args, **kwargs):
        if not self.pk:
            modifier = self.profile.streak*10
            self.stars = randint(10+modifier, 20+modifier)
            self.shares = randint(6+int(modifier/2), 12+int(modifier/2))
            profile = self.profile
            self._previous_image = None
            profile.addEntry()
            profile.save()
        else:
            self._previous_image = self.image.name
            
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

# Change entry image to oil painting after upload
@receiver(post_save, sender=Entry)
def modifyEntryImage(sender, instance, created, **kwargs):
    if hasattr(instance, '_previous_image') and instance._previous_image != instance.image:        
        img = cv2.imread(os.path.join(settings.MEDIA_ROOT, instance.image.name))
        filename = instance.image.name.split('/')[-1]
        res = cv2.xphoto.oilPainting(img, 9, 2)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT,entriesPhotosFolder, filename), res)
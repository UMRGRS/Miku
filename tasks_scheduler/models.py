from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Task(models.Model):
    title = models.CharField(('Titulo'), max_length=100)
    description = models.TextField(('Descripción'), max_length=200)
    dueDate = models.DateTimeField(('Fecha limite'), default=datetime.now()+timedelta(days=1))
    isCompleted = models.BooleanField(('Completada'), default=False)
    
class WSTask(Task):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    
class PTask(Task):
    class Priorities(models.TextChoices):
        urgent = 'UR', _('Urgente')
        high = 'HG', _('Alta')
        medium = 'MD', _('Media')
        low = 'LW', _('Baja')
    
    priority = models.CharField(('Prioridad'),max_length=2, choices=Priorities, default=Priorities.low)
    
class Subject(models.Model):
    name = models.CharField(('Materia'),max_length=40, unique=True)
    teacher = models.CharField(('Maestro'), max_length=100)
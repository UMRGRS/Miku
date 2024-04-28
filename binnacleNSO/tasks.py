from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from .models import Superuser

@db_periodic_task(crontab(hour='*24'))
def resetStreak():
    superusers = Superuser.objects.all()
    for user in superusers:
        user.resetStreak()
        user.save()
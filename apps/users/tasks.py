from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from users.models import CustomUser

@db_periodic_task(crontab(hour=0))
def resetStreak():
    users = CustomUser.objects.all()
    for user in users:
        user.resetStreak()
        user.save()
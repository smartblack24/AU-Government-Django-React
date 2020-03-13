from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from accounts.models import User

from gmailbox.utils import get_user_mails

logger = get_task_logger('mail')
@periodic_task(
    name="download_mails",
    run_every=(crontab(minute=0, hour='*/2'))
)
def download_mails():
    users = User.objects.filter(gmail_account__isnull=False)

    for user in users:
        logger.info("Started downloading mails for {}".format(user.full_name))

        res = get_user_mails(user)

        if res.get('success'):
            logger.info("Finished downloading mails for {}".format(user.full_name))
        else:
            logger.warning("Failed to download mails for {}".format(user.full_name))

        logger.info('-------------------------------')

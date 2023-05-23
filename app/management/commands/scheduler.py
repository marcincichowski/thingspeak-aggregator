from urllib import request

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.sites import requests
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
from django.core.management.base import BaseCommand
import logging
from django_apscheduler import util
import requests

from ...models import Thingspeaks, Measurement, MeasurementTypes

logger = logging.getLogger(__name__)


def parse_meta_field(fields_value, thingspeak):
    for field_value in fields_value:
        try:
            measurement_type = MeasurementTypes.objects.get(abbreviation=field_value, thingspeak=thingspeak)
        except MeasurementTypes.DoesNotExist:
            measurement_type = MeasurementTypes(abbreviation=field_value, thingspeak=thingspeak)
            measurement_type.save()


def deactivate_expired_accounts():
    thingspeaks = Thingspeaks.objects.all()
    if not thingspeaks:
        thingspeak = Thingspeaks.objects.create(channel=202842, name="L.2.7.14BT")
        thingspeak.save()
    if thingspeaks.count() == 1:
        thingspeak2 = Thingspeaks.objects.create(channel=202842, name="LAB2")
        thingspeak2.save()
    for thingspeak in thingspeaks:

        measurement_types = MeasurementTypes.objects.filter(thingspeak=thingspeak)
        measurements = Measurement.objects.filter(type__in=measurement_types)
        if measurements:
            latest = measurements.latest('created_date')
            response = requests.get('https://api.thingspeak.com/channels/' + str(thingspeak.channel) + '/feeds?'
                                                                                                       'start=' + str(
                latest.created_date))
        else:
            response = requests.get('https://api.thingspeak.com/channels/' + thingspeak.channel + '/feeds')
        fields = [v for k, v in response.json()['channel'].items() if k.startswith('field')]
        parse_meta_field(fields, thingspeak)
        for feed in response.json()['feeds']:
            fields_value = [v for k, v in feed.items() if k.startswith('field')]
            for i in range(0, len(fields_value)):
                print(fields[i], ' ', fields_value[i])
                if fields_value[i]:
                    measurement_type = MeasurementTypes.objects.get(abbreviation=fields[i], thingspeak=thingspeak)
                    measurement = Measurement(value=str(fields_value[i]).rstrip().replace("\"", ""), type=measurement_type,
                                              created_date=feed['created_at'])
                    measurement.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            deactivate_expired_accounts,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

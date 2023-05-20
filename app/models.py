from django.db import models


class Thingspeaks(models.Model):
    channel = models.CharField(max_length=6, null=False)
    name = models.CharField(max_length=30, null=False)


class MeasurementTypes(models.Model):
    thingspeak = models.ForeignKey(Thingspeaks, on_delete=models.CASCADE, null=False, related_name='thingspeak_server')

    abbreviation = models.CharField(null=False, max_length=50)


class Measurement(models.Model):
    type = models.ForeignKey(MeasurementTypes, on_delete=models.CASCADE, null=False, related_name='measurement_type')

    value = models.CharField(null=False, max_length=100)

    created_date = models.DateTimeField(null=False)

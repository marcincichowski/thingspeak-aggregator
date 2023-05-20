from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Measurement, Thingspeaks, MeasurementTypes


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class MeasurementSerializers(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = ['value', 'created_date']


class MeasurementTypesSerializer(serializers.ModelSerializer):
    measurement_type = MeasurementSerializers(read_only=True, many=True)

    class Meta:
        model = MeasurementTypes
        fields = '__all__'


class ThingspeakSerializers(serializers.ModelSerializer):
    thingspeak_server = MeasurementTypesSerializer(many=True, read_only=True)

    class Meta:
        model = Thingspeaks
        fields = '__all__'

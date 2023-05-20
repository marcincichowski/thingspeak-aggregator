from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer

from .models import MeasurementTypes, Measurement, Thingspeaks
from .serializers import UserSerializer, MeasurementTypesSerializer, MeasurementSerializers, ThingspeakSerializers
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class MeasurementTypeViewset(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):

    serializer_class = MeasurementTypesSerializer
    queryset = MeasurementTypes.objects.all()

    @action(detail=True, methods=['get'])
    def update_data(self, request, pk=True):
        instance = self.get_object()
        last_date = request.query_params.get('last_date')
        query = Measurement.objects.filter(type=instance, created_date__gt=last_date)
        print(instance.abbreviation)
        serializer = MeasurementSerializers(query, many=True)
        return Response(serializer.data)


class MeasurementViewset(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = MeasurementSerializers
    queryset = Measurement.objects.all()


class ThingspeaksApiViewset(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = ThingspeakSerializers
    queryset = Thingspeaks.objects.all()


class ThingspeaksViewset(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):

    serializer_class = ThingspeakSerializers
    queryset = Thingspeaks.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request,  *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'thingspeaks': serializer.data}, template_name='thingspeak_details.html')

    def list(self, request, *args, **kwargs):
        return Response({'thingspeaks': self.queryset},  template_name='index.html')

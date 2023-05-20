from django.contrib import admin
from django.urls import include, path

from . import views
from .viewsets import UserViewSet, ThingspeaksViewset, MeasurementTypeViewset, MeasurementViewset, ThingspeaksApiViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='users')
router.register(r'', ThingspeaksViewset, basename='thingspeaks')
router.register(r'api/measurement_types', MeasurementTypeViewset, basename='measurement_types')
router.register(r'api/measurements', MeasurementViewset, basename='measurements')
router.register(r'api/thingspeaks', ThingspeaksApiViewset, basename='api_thingspeaks')

urlpatterns = [
    path("", include(router.urls))
]


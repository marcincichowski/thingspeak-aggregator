# Generated by Django 4.2.1 on 2023-05-04 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=30)),
                ('abbreviation', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Thingspeaks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.JSONField()),
                ('thingspeak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thingspeak_server', to='app.thingspeaks')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurement_type', to='app.measurementtypes')),
            ],
        ),
    ]

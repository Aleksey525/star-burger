# Generated by Django 3.2.15 on 2024-09-11 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distance_monitor', '0008_alter_location_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='distance',
        ),
    ]

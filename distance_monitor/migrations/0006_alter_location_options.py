# Generated by Django 3.2.15 on 2024-09-11 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distance_monitor', '0005_alter_location_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'локация', 'verbose_name_plural': 'локации'},
        ),
    ]

# Generated by Django 3.2.15 on 2024-09-11 07:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_order_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='registrated_at',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, verbose_name='Дата и время создания'),
        ),
    ]

# Generated by Django 5.0.8 on 2024-09-05 12:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foodcartapp', '0050_order_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('lat', models.FloatField(null=True, verbose_name='Широта')),
                ('lon', models.FloatField(null=True, verbose_name='Долгота')),
                ('restaurant_name', models.CharField(max_length=100, verbose_name='Название ресторана')),
                ('distance', models.FloatField(default=0.0, verbose_name='Расстояние')),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата запроса к геокодеру')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='foodcartapp.order', unique=True)),
            ],
        ),
    ]

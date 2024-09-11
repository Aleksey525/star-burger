# Generated by Django 3.2.15 on 2024-09-11 12:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_alter_orderelements_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]

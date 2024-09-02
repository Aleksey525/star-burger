# Generated by Django 5.0.8 on 2024-08-26 14:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_orderelements_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
    ]
# Generated by Django 3.2.15 on 2024-08-06 06:42

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20210125_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Мобильный телефон')),
                ('address', models.CharField(max_length=50, verbose_name='адрес')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.order', verbose_name='Зааказ'),
        ),
    ]
from django.db import models
from django.utils import timezone

from foodcartapp.models import Order


class Location(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=100)
    order = models.ForeignKey(Order, related_name='locations', on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта', null=True)
    lon = models.FloatField(verbose_name='Долгота', null=True)
    restaurant_name = models.CharField(verbose_name='Название ресторана', max_length=100, null=True)
    distance = models.FloatField(verbose_name='Расстояние', default=0.0)
    last_updated = models.DateTimeField(verbose_name='Дата запроса к геокодеру', default=timezone.now)

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return self.address

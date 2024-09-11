from django.db import models
from django.utils import timezone


class Location(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=100)
    lat = models.FloatField(verbose_name='Широта', null=True)
    lon = models.FloatField(verbose_name='Долгота', null=True)
    last_updated = models.DateTimeField(verbose_name='Дата запроса к геокодеру', default=timezone.now)

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return self.address

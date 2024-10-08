from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models import F, Sum

from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class OrderQuerySet(models.QuerySet):
    def final_price(self):
        return self.annotate(price=Sum(F('elements__quantity') * F('elements__product__price')))


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )


    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    UNPROCESSED = 'Необработанный'
    IN_PROCESSING = 'Обрабатывается'
    IN_KITCHEN = 'Готовится'
    AT_COURIER = 'Передан курьеру'
    DELIVERED = 'Доставлен'
    ORDER_STATUSES = [
        (UNPROCESSED, 'Необработанный'),
        (IN_PROCESSING, 'Обрабатывается'),
        (IN_KITCHEN, 'Готовится'),
        (AT_COURIER, 'Передан курьеру'),
        (DELIVERED, 'Доставлен'),
    ]

    IN_CASH = 'Наличными'
    CASHLESS = 'Электронно'
    PAYMENT_METODS = [
        (IN_CASH, 'Наличными'),
        (CASHLESS, 'Электронно'),
    ]

    order_status = models.CharField(verbose_name='Статус заказа', max_length=50, choices=ORDER_STATUSES,
                                    default=UNPROCESSED, db_index=True, blank=True)
    firstname = models.CharField(verbose_name='Имя', max_length=50)
    lastname = models.CharField(verbose_name='Фамилия', max_length=50)
    phonenumber = PhoneNumberField(verbose_name='Мобильный телефон', db_index=True)
    address = models.CharField(verbose_name='адрес', max_length=50)
    comment = models.TextField(verbose_name='Комментарий', max_length=200, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата и время создания',
                                      auto_now_add=True, blank=True, db_index=True)
    called_at = models.DateTimeField(verbose_name='Дата звонка', null=True, blank=True, db_index=True)
    delivered_at = models.DateTimeField(verbose_name='Дата доставки', null=True, blank=True, db_index=True)
    payment_method = models.CharField(verbose_name='Способ оплаты', max_length=20, choices=PAYMENT_METODS,
                                      default=CASHLESS, blank=True, db_index=True)
    restaurant = models.ForeignKey(Restaurant, verbose_name='Ресторан', related_name='orders', blank=True, null=True,
                                   on_delete=models.CASCADE)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname}, {self.address}'


class OrderElements(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='elements', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='elements', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product.name}'











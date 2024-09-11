from django.conf import settings

from rest_framework.serializers import ModelSerializer
from distance_monitor.models import Location

from .models import Order, OrderElements, Product
from .utils import fetch_coordinates, get_restaurants


class OrderElementsSerializer(ModelSerializer):

    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def create(self, validated_data):
        product_fields = validated_data.pop('products')
        order_obj = Order.objects.create(**validated_data)
        YANDEX_API_KEY = settings.YANDEX_API_KEY
        order_address = validated_data.pop('address')
        delivery_coords = fetch_coordinates(YANDEX_API_KEY, order_address)
        Location.objects.get_or_create(address=order_address, lat=delivery_coords[0], lon=delivery_coords[1])

        for element in product_fields:
            product = Product.objects.get(name=element['product'])
            quantity = element['quantity']
            OrderElements.objects.create(order=order_obj, quantity=quantity, product=product, price=product.price)

        common_restaurants = get_restaurants(order_obj)

        for restaurant_name in common_restaurants:
            restaurant_coords = fetch_coordinates(YANDEX_API_KEY, restaurant_name)
            Location.objects.get_or_create(address=restaurant_name, lat=restaurant_coords[0], lon=restaurant_coords[1])

        return order_obj







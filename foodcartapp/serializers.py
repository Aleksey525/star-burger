from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ListField

from .models import Order, OrderElements, Product


class OrderElementsSerializer(ModelSerializer):

    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']



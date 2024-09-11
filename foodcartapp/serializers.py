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

    def create(self, validated_data):
        product_fields = validated_data.pop('products')
        order_obj = Order.objects.create(**validated_data)

        for element in product_fields:
            product = Product.objects.get(name=element['product'])
            quantity = element['quantity']
            OrderElements.objects.create(order=order_obj, quantity=quantity, product=product)
        return order_obj







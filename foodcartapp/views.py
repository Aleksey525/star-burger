from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.templatetags.static import static
from .models import Order, OrderElements
from rest_framework import status
import json


from .models import Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order = request.data
    if not 'products' in order.keys():
        content = {'products: Обязательное поле'}
    else:
        order_elements = order['products']
        if order_elements is None:
            content = {'products: Это поле не может быть пустым'}
        elif not isinstance(order_elements, list):
            content = {'products: Ожидался list со значениями, но был получен "str"'}
        elif len(order_elements) == 0:
            content = {'products: Этот список не может быть пустым'}
        else:
            name = order['firstname']
            lastname = order['lastname']
            phone = order['phonenumber']
            address = order['address']
            order_obj = Order.objects.create(name=name, last_name=lastname, phone=phone, address=address)

            for element in order_elements:
                product = Product.objects.get(pk=element['product'])
                quantity = element['quantity']
                OrderElements.objects.create(order=order_obj, quantity=quantity, product=product)
            return Response(order)
    return Response(content, status=status.HTTP_200_OK)

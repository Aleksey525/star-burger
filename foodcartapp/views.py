from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.templatetags.static import static
from .models import Order, OrderElements
from rest_framework import status
import re
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
    phone_pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    order = request.data
    if not 'products' in order.keys():
        content = {'products: Обязательное поле'}
    elif not ('firstname' and 'lastname' and 'phonenumber' and 'address') in order.keys():
        content = {'firstname, lastname, phonenumber, address: Обязательное поле'}
    else:
        order_elements = order['products']
        firstname = order['firstname']
        lastname = order['lastname']
        phonenumber = order['phonenumber']
        address = order['address']
        if order_elements is None:
            content = {'products: Это поле не может быть пустым'}
        elif not firstname and not lastname and not phonenumber and not address:
            content = {'firstname, lastname, phonenumber, address: Это поле не может быть пустым'}
        elif firstname is None:
            content = {'firstname: Это поле не может быть пустым'}
        elif not phonenumber:
            content = {'phonenumber: Это поле не может быть пустым'}
        elif not re.match(phone_pattern, phonenumber):
            content = {'phonenumber: Введен некорректный номер телефона'}
        elif not isinstance(firstname, str):
            content = {'firstname: Not a valid string'}
        elif not isinstance(order_elements, list):
            content = {'products: Ожидался list со значениями, но был получен "str"'}
        elif len(order_elements) == 0:
            content = {'products: Этот список не может быть пустым'}
        else:
            order_obj = Order.objects.create(firstname=firstname, lastname=lastname, phonenumber=phonenumber, address=address)
            for element in order_elements:
                product = Product.objects.get(pk=element['product'])
                quantity = element['quantity']
                OrderElements.objects.create(order=order_obj, quantity=quantity, product=product)
            return Response(order)
    return Response(content, status=status.HTTP_200_OK)

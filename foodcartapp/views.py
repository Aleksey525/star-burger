from django.http import JsonResponse
from django.templatetags.static import static
from .models import Order, OrderElements
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


def register_order(request):
    try:
        order = json.loads(request.body.decode())
        name = order['firstname']
        lastname = order['lastname']
        phone = order['phonenumber']
        address = order['address']
        order_elements = order['products']
        order_obj = Order.objects.create(name=name, last_name=lastname, phone=phone, address=address)
        for element in order_elements:
            product = Product.objects.get(pk=element['product'])
            quantity = element['quantity']
            OrderElements.objects.create(order=order_obj, quantity=quantity, product=product)
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })
    return JsonResponse({})

from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
import requests


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from geopy.distance import geodesic
from django.conf import settings


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def calculate_distance(restaurant_coords, delivery_coords):
    return geodesic(restaurant_coords, delivery_coords).kilometers


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = Order.objects.final_price().prefetch_related(
        'elements__product__menu_items__restaurant').all()

    for order in order_items:
        restaurant_dist = {}
        all_products_available = True
        product_restaurants_sets = []
        for order_product in order.elements.all():
            product_restaurants = set()
            for menu_item in order_product.product.menu_items.all():
                if menu_item.availability:
                    product_restaurants.add(menu_item.restaurant.name)
            if not product_restaurants:
                all_products_available = False
                break
            product_restaurants_sets.append(product_restaurants)
        if all_products_available:
            common_restaurants = set.intersection(*product_restaurants_sets)
            for restaurant_name in common_restaurants:
                try:
                    YANDEX_API_KEY = settings.YANDEX_API_KEY
                    restaurant_coords = fetch_coordinates(YANDEX_API_KEY , restaurant_name)
                    delivery_coords = fetch_coordinates(YANDEX_API_KEY, order.address)
                    if restaurant_coords and delivery_coords:
                        distance = calculate_distance(restaurant_coords, delivery_coords)
                        restaurant_dist[restaurant_name] = distance
                except Exception as error:
                    print(f"Ошибка получения координат для {restaurant_name}: {error}")

            order.restaurants = common_restaurants

        if restaurant_dist:
            closest_restaurant = min(restaurant_dist, key=restaurant_dist.get)
            order.closest_restaurant = closest_restaurant
            order.closest_distance = restaurant_dist[closest_restaurant]
        else:
            order.closest_restaurant = None
            order.closest_distance = None

    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
    })

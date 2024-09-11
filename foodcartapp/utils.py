import requests


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


def get_restaurants(order):
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
    return common_restaurants

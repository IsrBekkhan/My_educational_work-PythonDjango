from timeit import default_timer
from datetime import date, datetime

from django.shortcuts import render
from django.http import HttpRequest

from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ("note", 500),
        ("book", 1000),
        ("pencil", 100),
    ]
    context = {
        "time_running": default_timer(),
        "current_date": date.today(),
        "timestamp": datetime.today().timestamp(),
        "products": products
    }
    return render(request, "shopapp/shop-index.html", context=context)


def get_products(request: HttpRequest):
    products = {
        "products": Product.objects.all(),
    }
    return render(request, "shopapp/products-list.html", context=products)


def get_orders(request: HttpRequest):
    orders = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, "shopapp/orders-list.html", context=orders)

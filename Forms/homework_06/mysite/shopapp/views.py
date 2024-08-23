from timeit import default_timer
from datetime import date, datetime

from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse

from .models import Product, Order
from .forms import ProductForm, OrderForm


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


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()

    context = {
        "form": form
    }
    return render(request, "shopapp/create-product.html", context=context)


def get_orders(request: HttpRequest):
    orders = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, "shopapp/orders-list.html", context=orders)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        "form": form
    }
    return render(request, "shopapp/order_form.html", context=context)




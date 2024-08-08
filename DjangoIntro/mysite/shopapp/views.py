from timeit import default_timer
from datetime import date, datetime


from django.shortcuts import render
from django.http import HttpRequest


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

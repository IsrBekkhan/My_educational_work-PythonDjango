from django.urls import path

from .views import shop_index, get_orders, get_products

app_name = "shopapp"
urlpatterns = [
    path("", shop_index, name="index"),
    path("products", get_products, name="products"),
    path("orders", get_orders, name="orders"),
]


from django.urls import path

from .views import shop_index, get_orders, get_products, create_product, create_order

app_name = "shopapp"
urlpatterns = [
    path("", shop_index, name="index"),
    path("products", get_products, name="products_list"),
    path("products/create", create_product, name="product_create"),
    path("orders", get_orders, name="orders_list"),
    path("orders/create", create_order, name="order_create"),
]


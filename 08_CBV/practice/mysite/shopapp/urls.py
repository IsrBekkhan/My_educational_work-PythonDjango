from django.urls import path

from .views import (
    create_order,
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductsListView,
    OrdersListView,
    OrdersDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = "shopapp"
urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create/", create_order, name="order_create"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details")
]


from timeit import default_timer
from datetime import date, datetime

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order
from .forms import ProductForm, OrderForm, GroupForm


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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


# def shop_index(request: HttpRequest):
#     products = [
#         ("note", 500),
#         ("book", 1000),
#         ("pencil", 100),
#     ]
#     context = {
#         "time_running": default_timer(),
#         "current_date": date.today(),
#         "timestamp": datetime.today().timestamp(),
#         "products": products
#     }
#     return render(request, "shopapp/shop-index.html", context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)

# def groups_list(request: HttpRequest):
#     context = {
#         "groups": Group.objects.prefetch_related('permissions').all(),
#     }
#     return render(request, 'shopapp/groups-list.html', context=context)


# ======products_detail на базе класса DetailView======
class ProductDetailView(DetailView):
    template_name = "shopapp/product_detail.html"
    model = Product
    context_object_name = "product"


# ======products_detail на базе класса View======
# class ProductDetailView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             "product": product
#         }
#         return render(request, "shopapp/product_detail.html", context=context)


# ======products_list на базе класса ListView======
class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


# ======products_list на базе класса TemlateView======
# class ProductsListView(TemplateView):
#     template_name = "shopapp/product_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context

# ======products_list на базе функции======
# def get_products(request: HttpRequest):
#     products = {
#         "products": Product.objects.all(),
#     }
#     return render(request, "shopapp/product_list.html", context=products)


# ======product_create на базе класса CreateView ======
class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    # form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")


# ======product_create на базе функции ======
# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#
#         if form.is_valid():
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shopapp:products_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {
#         "form": form
#     }
#     return render(request, "shopapp/create-product.html", context=context)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )


# full delete product
# class ProductDeleteView(DeleteView):
#     model = Product
#     success_url = reverse_lazy("shopapp:products_list")


# soft delete product
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


# ======orders_list на базе класса ListView ======
class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


# ======orders_list на базе функции======
# def get_orders(request: HttpRequest):
#     orders = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#     }
#     return render(request, "shopapp/order_list.html", context=orders)


class OrdersDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


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




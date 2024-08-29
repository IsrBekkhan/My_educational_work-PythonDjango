from timeit import default_timer
from datetime import date, datetime

from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from .models import Product, Order
from .forms import OrderForm, GroupForm


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


class ProductsListView(ListView):
    queryset = Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    queryset = Product.objects.filter(archived=False)


# class ProductCreateView(UserPassesTestMixin, CreateView):
#     model = Product
#     fields = "name", "price", "description", "discount"
#     success_url = reverse_lazy("shopapp:product_list")
#
#     def test_func(self):
#         # return self.request.user.groups.filter(name="secret-group").exists()
#         return self.request.user.is_superuser


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:product_list")
    permission_required = ["shopapp.add_product", ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk}
        )

    def test_func(self):
        product = self.get_object()
        return (
                self.request.user.is_superuser or
                (self.request.user == product.created_by and self.request.user.has_perm("shopapp.change_product"))
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:product_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ["shopapp.view_order", ]
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    template_name = "shopapp/order_form.html"
    fields = "delivery_address", "promo_code", "user", "products"
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    template_name = "shopapp/order_update_form.html"
    fields = "delivery_address", "promo_code", "user", "products"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")
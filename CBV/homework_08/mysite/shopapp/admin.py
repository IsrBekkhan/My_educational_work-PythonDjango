from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archived products")
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchived products")
def mark_unarchived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "short_description", "price", "discount", "created_at", "archived"
    list_display_links = "pk", "name"
    search_fields = "price", "name"
    ordering = "pk", "name"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "description": "Цена продукта с возможной скидкой.",
        }),
        ("Extra options", {
            "fields": ("archived", ),
            "classes": ("collapse", ),
            "description": "Field 'archived' is for soft delete."
        })
    ]

    @staticmethod
    def short_description(obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


# class ProductInline(admin.StackedInline):
class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "pk", "delivery_address", "promo_code", "created_at", "user_verbose"
    list_display_links = "pk", "user_verbose"
    ordering = "pk", "created_at"
    search_fields = "pk", "delivery_address"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    @staticmethod
    def user_verbose(obj: Order) -> str:
        return obj.user.first_name or obj.user.username


# admin.site.register(Product, ProductAdmin)
# admin.site.register(Order, OrderAdmin)


@admin.action(description="Archived products")
def mark_archived(model_admin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

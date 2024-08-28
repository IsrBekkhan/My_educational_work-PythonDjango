from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    # @property
    # def short_description(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"{self.id}. {self.name}"


class Order(models.Model):
    class Meta:
        ordering = ["created_at"]

    delivery_address = models.TextField(null=False, blank=True)
    promo_code = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")

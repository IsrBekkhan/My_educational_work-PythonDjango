from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Order, Product


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         self.stdout.write("Create order")
#         user = User.objects.get(username="admin")
#         order = Order.objects.get_or_create(
#             delivery_address="ul Pupkina, d 8",
#             promocode="SALE123",
#             user=user,
#         )
#         self.stdout.write(f"Created order {order}")


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        # with transaction.atomic():
        #     ...
        self.stdout.write("Create order with products")
        user = User.objects.get(username="bekkhan")
        # метод defer - накладывает на указанные поля ленивую загрузку
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        # метод only - накладывает ленивую загрузку на все поля, кроме указанных
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address="New address, D07",
            promocode="promo5",
            user=user,
        )
        for product in products:
            order.products.add(product)
        self.stdout.write(f"Created order {order}")

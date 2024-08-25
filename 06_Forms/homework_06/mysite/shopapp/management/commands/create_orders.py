from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product, Order


class Command(BaseCommand):
    """
    Creates orders
    """
    def handle(self, *args, **options):
        self.stdout.write("Creating orders...")

        products = Product.objects.all()
        user = User.objects.get()
        order, created = Order.objects.get_or_create(
            delivery_address="Гагарина, Дом 3",
            promo_code="DJANGO",
            user=user,
        )
        order = Order.objects.first()

        for product in products:
            order.products.add(product)

            self.stdout.write(f"Ordering a {product.name} for the {user.username} created")
        order.save()

        self.stdout.write(self.style.SUCCESS(f"All products created to order for the {user.username}!"))

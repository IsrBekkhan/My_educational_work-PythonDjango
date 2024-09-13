from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start demo select fields")

        product_values = Product.objects.values("pk", "name",)
        for p_values in product_values:
            print(p_values)

        users_info = User.objects.values_list("pk", "username")
        for user_info in users_info:
            print(user_info)

        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))

        self.stdout.write("Done!")

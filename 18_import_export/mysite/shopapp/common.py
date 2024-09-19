from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    for row in reader:
        order, create = Order.objects.get_or_create(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            user_id=row["user_id"],
        )
        for product_id in row["product_id"].split(";"):
            try:
                order.products.add(Product.objects.get(pk=product_id))
            except Product.DoesNotExist:
                pass

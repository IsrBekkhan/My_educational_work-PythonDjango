from string import ascii_letters
from random import choices

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse

from .utils import add_two_numbers
from .models import Product, Order


class OrderDetailView(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="".join(choices(ascii_letters, k=6)),
            password="".join(choices(ascii_letters, k=8)),
        )
        view_order_perm = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(view_order_perm)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="Test delivery address",
            promocode="SKILL",
            user=self.user,
        )
        for product in Product.objects.all():
            self.order.products.add(product)
        self.order.save()

    def tearDown(self):
        self.order.delete()

    def test_order_detail(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["object"].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = [
        "users_fixtures.json",
        "products_fixtures.json",
        "orders_fixtures.json"
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="".join(choices(ascii_letters, k=6)),
            password="".join(choices(ascii_letters, k=8)),
            is_staff=True,
        )
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_export_view(self):
        response = self.client.get(
            reverse("shopapp:orders_export")
        )

        orders = (Order.objects.order_by("pk")
                  .select_related("user")
                  .prefetch_related("products")
                  .all())
        expected_data = [
            {
                "id": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user.pk,
                "products": [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        orders_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(orders_data["orders"], expected_data)


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create_view(self):
        response: HttpResponse = self.client.post(
            reverse("shopapp:product_create"),
            data={
                "name": self.product_name,
                "price": "123.45",
                "description": "New car!",
                "discount": "10"
            }
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name="Some product")
    #
    # def tearDown(self) -> None:
    #     self.product.delete()

    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Some product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        "products_fixtures.json",
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))

        # for product in Product.objects.filter(archived=False).all():
        #     self.assertContains(response, product.name)

        # products = Product.objects.filter(archived=False).all()
        # products_ = response.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)

        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products-list.html")


class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # cls.credentials = dict(username="Bob_test", password="qwerty")
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        # self.assertRedirects(response, str(settings.LOGIN_URL))
        self.assertEqual(response.status_code, 302)
        print(str(settings.LOGIN_URL))
        print(response.url)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        "products_fixtures.json",
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products_export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )
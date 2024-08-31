import json
from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response: HttpResponse = self.client.get(reverse("myauth:cookie-get"))
        print(response.content.decode())
        self.assertContains(response, "Cookie value")


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        response: HttpResponse = self.client.get(reverse("myauth:foo-bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], "application/json",
        )
        expected_date = {"foo": "bar", "spam": "eggs"}
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expected_date)
        self.assertJSONEqual(response.content, expected_date)

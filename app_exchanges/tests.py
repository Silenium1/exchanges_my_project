from django.test import (
    TestCase,
    Client,
)  # https://docs.djangoproject.com/en/4.2/topics/testing/tools/

# To use the test client, instantiate django.test.Client and retrieve web pages
# unittest.TestCase. unittest.TestCase is a class from Python's standard library,
# Client is a class that can simulate a user interacting with the code at the view level.
# It can be used to test that views are working as expected.
from django.urls import reverse

# Importing the reverse function, which is used to reverse-resolve URLs.
# Given the name of a URL pattern, it will return the URL string.
# This is useful in tests to avoid hardcoding URLs.
from .models import (
    Exchange,
    Commodity,
    Currency,
    Exchanges_Commodities,
    Exchanges_Currencies,
)


class MainViewTest(TestCase):
    def setUp(
        self,
    ):  # https://docs.python.org/3/library/unittest.html#unittest.TestCase
        # Method called to prepare the test fixture.
        # This is called immediately before calling the test method; other than AssertionError or SkipTest,
        # any exception raised by this method will be considered an error rather than a test failure.
        # The default implementation does nothing.

        self.client = Client()  # Creating an instance of the
        # Client class, which can be used to simulate GET and POST requests among others

        # You can add setup data for your models here
        self.exchange = Exchange.objects.create(
            exchange_abbr="EX", exchange_name="Exchange1"
        )
        self.commodity = Commodity.objects.create(
            commodity_ticker_name="CTN",
            commodity_descr="Commodity1",
            unit_int_value=1,
            unit_str_value="KG",
        )
        self.currency = Currency.objects.create(
            currency_ticker_name="CTN", currency_descr="Currency1", type="SPOT"
        )

        self.exchanges_commodities = Exchanges_Commodities.objects.create(
            exchange=self.exchange, commodity_ticker_name=self.commodity, price=100
        )
        self.exchanges_currencies = Exchanges_Currencies.objects.create(
            exchange=self.exchange,
            currency_ticker_name=self.currency,
            base_currency="USD",
            new_currency="EUR",
            tenor_months="1 M",
            price=200,
        )

    def test_main_view(self):
        response = self.client.get(reverse("main_view"))  # Using the client
        # to send a GET request to the URL that is named 'main_view'

        # Assert status code
        self.assertEqual(response.status_code, 200)

        # Assert context data (You can add checks for data in your context)
        self.assertTrue("all_tickers" in response.context)
        self.assertTrue("currency_types" in response.context)

        # Assert template used
        self.assertTemplateUsed(response, "main.html")

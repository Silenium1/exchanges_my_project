from django.test import TestCase, Client
from django.urls import reverse
from .models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from .forms import ExchangeForm, CommodityForm, CurrencyForm, ExchangesCommoditiesForm


class PagesTest(TestCase): # class to test different pages

    def test_main_view(self): # test the main page
        response = self.client.get(reverse('main_view'))
        self.assertEqual(response.status_code, 200)

    def test_asset_class_view_commodity(self): # test the commodity ticker page
        asset_class = 'commodity'
        ticker = 'palm-oil'
        id_ticker_id = 3
        url = reverse('asset_class_view', args=[asset_class, ticker, id_ticker_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_asset_class_view_currency(self): # test the currency ticker page
        asset_class = 'currency'
        ticker = 'hong-kong-dollar-3-month-forward'
        id_ticker_id = 2
        url = reverse('asset_class_view', args=[asset_class, ticker, id_ticker_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_exchange(self): #testing adding and deleting Exchanges

        response = self.client.post(reverse('admin_dashboard'), {
            'exchange_abbr': 'NYSE',
            'exchange_name': 'New York Stock Exchange',
            'exchange': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Exchange.objects.count(), 1)

    def test_form_commodity(self): #testing adding and deleting Commodities
        response = self.client.post(reverse('admin_dashboard'), {
            'commodity_ticker_name': 'test',
            'commodity_descr': 'test2',
            'unit_int_value': 4,
            'unit_str_value': 'kg',
            'commodity': ''

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commodity.objects.count(), 1)


    def test_form_currency(self): #testing adding and deleting Currencies
        response = self.client.post(reverse('admin_dashboard'), {
            'currency_ticker_name': 'test',
            'currency_descr': 'test2',
            'type': 'SPOT',
            'currency': ''

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Currency.objects.count(), 1)



    def test_form_exchanges_commodities(self): #testing adding and deleting Commodity Tickers
        self.exchange = Exchange.objects.create(exchange_abbr="NYSE", exchange_name="New York Stock Exchange")
        self.commodity = Commodity.objects.create(commodity_ticker_name="COM", commodity_descr="Commodity Description",
                                             unit_int_value=1, unit_str_value="One")

        response = self.client.post(reverse('admin_dashboard'), {
            'exchanges_commodities': 'any_value',
            'exchange': self.exchange.id,
            'commodity_ticker_name': self.commodity.id,
            'time_of_last_trade': "12:00",
            'price': 100
        })


        self.assertEqual(response.status_code, 302)
        self.assertEqual(Exchanges_Commodities.objects.count(), 1)

    def test_form_exchanges_currencies(self): #testing adding and deleting Currency Tickers
        self.exchange = Exchange.objects.create(exchange_abbr="NYSE", exchange_name="New York Stock Exchange")
        self.currency_ticker_name = Currency.objects.create(currency_ticker_name="USD GBR FORWARD",
                                                currency_descr="USD GBR FORWARD", type="SPOT")

        response = self.client.post(reverse('admin_dashboard'), {
                'exchanges_currencies': 'any_value',
                'exchange': self.exchange.id,
                'currency_ticker_name': self.currency_ticker_name.id,
                'base_currency': "USD",
                'new_currency' : "EUR",
                'tenor_months' : "1 M",
                'settlement_date' : "01.12.2022",
                'settlement_date_swap': 'test',
                'price' : 100
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Exchanges_Currencies.objects.count(), 1)

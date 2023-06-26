from django.test import TestCase, Client
from django.urls import reverse
from .models import Exchange, Commodity, Currency, Exchanges_Commodities
from .forms import ExchangeForm, CommodityForm, CurrencyForm, ExchangesCommoditiesForm

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_submission(self):
        # test exchange form
        response = self.client.post(reverse('admin_dashboard'), {
            'exchange_abbr': 'NYSE',
            'exchange_name': 'New York Stock Exchange',
            'exchange': ''
        })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Exchange.objects.count(), 1)  # ensure form data saved

        # test commodity form
        response = self.client.post(reverse('admin_dashboard'), {
            'commodity_ticker_name': 'COM1',
            'commodity_descr': 'First Commodity',
            'unit_int_value': 1,
            'unit_str_value': 'One unit',
            'commodity': ''
        })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Commodity.objects.count(), 1)

        # test currency form
        response = self.client.post(reverse('admin_dashboard'), {
            'currency_ticker_name': 'CUR1',
            'currency_descr': 'First Currency',
            'type': 'SPOT',
            'currency': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Currency.objects.count(), 1)

        # test exchanges_commodities form
        exchange_id = Exchange.objects.first().id
        commodity_id = Commodity.objects.first().id
        response = self.client.post(reverse('admin_dashboard'), {
            'exchange': exchange_id,
            'commodity': commodity_id,
            'time_of_last_trade': '2023-06-01',
            'price': 100,
            'exchanges_commodities': ''
        })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Exchanges_Commodities.objects.count(), 1)

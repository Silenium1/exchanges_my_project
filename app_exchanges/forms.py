# forms.py

from django import forms
from .models import (
    Exchange,
    Commodity,
    Currency,
    Exchanges_Commodities,
    Exchanges_Currencies,
)


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ["exchange_abbr", "exchange_name"]


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = [
            "commodity_ticker_name",
            "commodity_descr",
            "unit_int_value",
            "unit_str_value",
        ]


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ["currency_ticker_name", "currency_descr", "type"]


class ExchangesCommoditiesForm(forms.ModelForm):
    class Meta:
        model = Exchanges_Commodities
        fields = ["exchange", "commodity_ticker_name", "time_of_last_trade", "price"]


class ExchangesCurrenciesForm(forms.ModelForm):
    class Meta:
        model = Exchanges_Currencies
        fields = [
            "exchange",
            "currency_ticker_name",
            "base_currency",
            "new_currency",
            "tenor_months",
            "settlement_date",
            "settlement_date_swap",
            "price",
        ]

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


class Exchange(models.Model):
    id = models.AutoField(primary_key=True)
    exchange_abbr = models.CharField(max_length=70)
    exchange_name = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.exchange_abbr} {self.exchange_name}"


class Commodity(models.Model):
    id = models.AutoField(primary_key=True)
    commodity_ticker_name = models.CharField(max_length=70)
    commodity_descr = models.CharField(max_length=70, null=True)
    unit_int_value = models.IntegerField(null=True)
    unit_str_value = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"

    def __str__(self):
        return f"{self.commodity_ticker_name}"


class Currency(models.Model):
    SPOT = "SPOT"
    FORWARD = "FORWARD"
    SWAP = "SWAP"
    currency_ticker_types = [(SPOT, "SPOT"), (FORWARD, "FORWARD"), (SWAP, "SWAP")]
    id = models.AutoField(primary_key=True)
    currency_ticker_name = models.CharField(max_length=50)
    currency_descr = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=15, choices=currency_ticker_types, default=SPOT)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.currency_ticker_name} {self.type}"


class Exchanges_Commodities(models.Model):
    id = models.AutoField(primary_key=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    commodity_ticker_name = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    time_of_last_trade = models.DateField(null=True, blank=True)
    price = models.IntegerField()


class Exchanges_Currencies(models.Model):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    currency_list = [(USD, "USD"), (EUR, "EUR"), (GBP, "GBP")]
    M1 = "1 M"
    M2 = "2 M"
    M3 = "3 M"
    tenor_options = [(M1, "1 M"), (M2, "2 M"), (M3, "3 M")]

    id = models.AutoField(primary_key=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    currency_ticker_name = models.ForeignKey(Currency, on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=15, choices=currency_list, default=USD)
    new_currency = models.CharField(max_length=15, choices=currency_list, default=USD)
    tenor_months = models.CharField(max_length=15, choices=tenor_options, default="--")
    settlement_date = models.DateField(null=True, blank=True)
    settlement_date_swap = models.DateField(null=True, blank=True)
    price = models.IntegerField()

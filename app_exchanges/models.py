from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator,ValidationError



class Exchange(models.Model):
    exchange_abbr = models.CharField(max_length=70)
    exchange_name = models.CharField(max_length=70)

    def __str__(self):
        return f'{self.exchange_abbr} {self.exchange_name}'

    def save(self, *args, **kwargs):
        # Check for duplicate exchange abbreviation
        if not self.pk and Exchange.objects.filter(exchange_abbr=self.exchange_abbr).exists():
            self.errors = 'Exchange abbreviation already exists.'
            return
        # Check for duplicate exchange name
        if not self.pk and Exchange.objects.filter(exchange_name=self.exchange_name).exists():
            self.errors = 'Exchange name already exists.'
            return
        super().save(*args, **kwargs)


class Commodity(models.Model):
    commodity_ticker_name = models.CharField(max_length=70)
    commodity_descr = models.CharField(max_length=70, null=True)
    unit_int_value = models.IntegerField(null=True)
    unit_str_value = models.CharField(max_length=50,null=True)

    class Meta:
        verbose_name = 'Commodity'
        verbose_name_plural = 'Commodities'

    def __str__(self):
        return f'{self.commodity_ticker_name}'



class Currency(models.Model):
    SPOT = 'SPOT'
    FORWARD = 'FORWARD'
    SWAP = 'SWAP'
    currency_ticker_types = [
        (SPOT, 'SPOT'),
        (FORWARD, 'FORWARD'),
        (SWAP, 'SWAP')
    ]
    currency_ticker_name = models.CharField(max_length=50)
    currency_descr = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=15, choices=currency_ticker_types, default=SPOT)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f'{self.currency_ticker_name} {self.type}'


class Exchanges_Commodities(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    commodity_ticker_name = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    time_of_last_trade =models.CharField(max_length=30, null=True)
    price = models.IntegerField()


class Exchanges_Currencies(models.Model):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    currency_list = [
        (USD, 'USD'),
        (EUR, 'EUR'),
        (GBP, 'GBP')
    ]
    M1 = '1 M'
    M2 = '2 M'
    M3 = '3 M'
    tenor_options = [
        (M1, '1 M'),
        (M2, '2 M'),
        (M3, '3 M')
    ]

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    currency_ticker_name = models.ForeignKey(Currency, on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=15, choices=currency_list, default=USD)
    new_currency = models.CharField(max_length=15, choices=currency_list, default=USD)
    tenor_months = models.CharField(max_length=15, choices=tenor_options, default='--')
    settlement_date = models.CharField(max_length=30, null=True)
    settlement_date_swap = models.CharField(max_length=30, null=True)
    price = models.IntegerField()




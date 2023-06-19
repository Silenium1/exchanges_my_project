from django.shortcuts import render
from django.http import Http404
from .models import Asset_class, Exchange,Ticker,Commodity, Currency

def generate_all_tickers():
    all_tickers = {}
    for ticker in Ticker.objects.all():
        asset_class = Asset_class.objects.get(id=ticker.asset_class_id)
        commodity = Commodity.objects.get(ticker=ticker)
        currency = Currency.objects.get(ticker=ticker)
        where_to_buy = {commodity.exchange_name: commodity.price}
        all_tickers[ticker.ticker_name] = {
            'name': ticker.ticker_name,
            'asset_class': asset_class.asset_class,
            'where_to_buy': where_to_buy,
            'descr': ticker.ticker_descr,
            'unit': f"{commodity.unit_int_value} {commodity.unit_str_value}",
            'Time of last trade': ticker.time_of_last_trade,
            'type': currency.type,
            'tenor': currency.tenor_months,
        }
    return all_tickers
from app_exchanges.models import Exchanges_Commodities, Exchanges_Currencies
from dataclasses import dataclass


# function to retrieve all tickers in our database
def get_all_tickers() -> dict:
    commodity_exchanges = Exchanges_Commodities.objects.all()  # fetching all commodity tickers
    # from Exchanges_Commodities class
    all_tickers = {}  # creating a dictionary to manipulate our data
    for commodity in commodity_exchanges:  # iterate through objects or retrieved data
        key = (1, commodity.commodity_ticker_name.id)  # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            'exchange': commodity.exchange.exchange_name,  # storing a name of an exchange
            'asset_class': 'Commodity',  # storing a name of our asset class
            'ticker': commodity.commodity_ticker_name.commodity_ticker_name,  # storing a name of the ticker
            'price': commodity.price,  # storing a current price
        }

    currency_exchanges = Exchanges_Currencies.objects.all()  # fetching all commodity tickers from Exchanges_Currencies
    for currency in currency_exchanges:  # iterate through objects or retrieved data
        key = (2, currency.currency_ticker_name.id)  # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            'exchange': currency.exchange.exchange_name,  # storing a name of an exchange
            'asset_class': 'Currency',  # storing a name of our asset class
            'ticker': currency.currency_ticker_name.currency_ticker_name,  # storing a name of the ticker
            'price': currency.price,  # storing a current price
            'tenor': currency.tenor_months,  # storing Tenor date
            'currency_type': currency.currency_ticker_name.type  # storing a currency type
        }

    return all_tickers


# function to filter based on a user's behavior
def filter_tickers(all_tickers, selected_asset_classes, currency_types) -> dict:
    filtered_tickers = {}  # create a dictionary to store filtered tickers

    if "all" in selected_asset_classes or not selected_asset_classes:
        filtered_tickers = all_tickers  # don't filter anything if either 'ALL" is chosen or nothing is chosen
    else:
        for key, value in all_tickers.items():  # filter by asset class
            if value['asset_class'] in selected_asset_classes:
                filtered_tickers[key] = value

    if currency_types:  # filter by currency type
        filtered_tickers = {
            key: value for key, value in filtered_tickers.items()
            if 'currency_type' in value and value['currency_type'] in currency_types
        }

    return filtered_tickers


# function to retrieve data specifically for one ticker
def asset_class_view_filter(asset_class, ticker, id_ticker_id) -> dict:
    currency_type = ''
    current_ticker = {}
    if asset_class == 'commodity':
        commodity_exchanges = Exchanges_Commodities.objects.filter(commodity_ticker_name__id=id_ticker_id)
        # fetching the commodity ticker with this ticker id
        for commodity in commodity_exchanges:  # iterate through to get all the data for this commodity ticker
            key = (commodity.exchange.id, commodity.commodity_ticker_name.id)  # hashmap Exchange ID / commodity ID
            current_ticker[key] = {
                'exchange': commodity.exchange.exchange_name,
                'asset_class': 'commodity',
                'ticker': commodity.commodity_ticker_name.commodity_ticker_name,
                'ticker_descr': commodity.commodity_ticker_name.commodity_descr,
                'price': commodity.price,
                'unit_int_value': commodity.commodity_ticker_name.unit_int_value,
                'unit_str_value': commodity.commodity_ticker_name.unit_str_value,
                'time_of_last_trade': commodity.time_of_last_trade
            }

    else:
        currency_exchanges = Exchanges_Currencies.objects.filter(currency_ticker_name__id=id_ticker_id)
        # fetching the currency ticker with this ticker id
        for currency in currency_exchanges:  # iterate through to get all the data for this currency ticker
            key = (currency.exchange_id, currency.currency_ticker_name_id)  # hashmap Exchange ID / currency ID
            current_ticker[key] = {
                'exchange': currency.exchange.exchange_name,
                'asset_class': 'currency',
                'ticker': currency.currency_ticker_name.currency_ticker_name,
                'price': currency.price,
                'tenor': currency.tenor_months,
                'ticker_descr': currency.currency_ticker_name.currency_descr,
                'settlement_date': currency.settlement_date
                if currency.settlement_date is not None else 'N/A',
                'settlement_date_swap': currency.settlement_date

            }
            currency_type = currency.currency_ticker_name.type

    return current_ticker if asset_class == 'commodity' else [current_ticker, currency_type]
    # return just the ticker or ticker + currency type for currency

from django.shortcuts import render

from django.shortcuts import redirect
from .models import (
    Exchange,
    Commodity,
    Currency,
    Exchanges_Commodities,
    Exchanges_Currencies,
)

from .forms import CommodityForm
from .forms import ExchangeForm
from .forms import CurrencyForm
from .forms import ExchangesCommoditiesForm

asset_classes = {"commodity", "currency"}

# def asset_class_redirect(request, asset_class):
#     return redirect('main_view')


def asset_class_view(request, asset_class, ticker, id_ticker_id):
    current_ticker = {}  # dictionary to store a current ticket info
    currency_type = ""  # declare a variable to save a currency type
    ticker_descr = ""
    # currency = Currency.objects.get(id=id_ticker_id)  #fetching currency data with the current ticker ID
    # currency_type = currency.type # getting a current currency type
    if asset_class == "commodity":
        commodity_exchanges = Exchanges_Commodities.objects.filter(
            commodity_ticker_name__id=id_ticker_id
        )
        # fetchinG a currency ticker with this ticker id

        for (
            commodity
        ) in (
            commodity_exchanges
        ):  # iterate through to get all the data for this commodity ticker
            key = (
                commodity.exchange.id,
                commodity.commodity_ticker_name.id,
            )  # hashmap Exchange ID / commodity ID
            current_ticker[key] = {
                "exchange": commodity.exchange.exchange_name,
                "asset_class": "commodity",
                "ticker": commodity.commodity_ticker_name.commodity_ticker_name,
                "ticker_descr": commodity.commodity_ticker_name.commodity_descr,
                "price": commodity.price,
                "unit_int_value": commodity.commodity_ticker_name.unit_int_value,
                "unit_str_value": commodity.commodity_ticker_name.unit_str_value,
                "time_of_last_trade": commodity.time_of_last_trade,
            }

        return render(
            request,
            "app_exchanges/commodities/commodity_prices.html",
            context={
                "current_ticker": current_ticker,
                "ticker_descr": ticker_descr,
                "ticker": ticker,
            },
        )

    elif asset_class == "currency":
        currency_exchanges = Exchanges_Currencies.objects.filter(
            currency_ticker_name__id=id_ticker_id
        )

        for (
            currency
        ) in (
            currency_exchanges
        ):  # iterate through to get all the data for this currency ticker
            key = (
                currency.exchange_id,
                currency.currency_ticker_name_id,
            )  # hashmap Exchange ID / currency ID
            current_ticker[key] = {
                "exchange": currency.exchange.exchange_name,
                "asset_class": "currency",
                "ticker": currency.currency_ticker_name.currency_ticker_name,
                "price": currency.price,
                "tenor": currency.tenor_months,
                "ticker_descr": currency.currency_ticker_name.currency_descr,
                "settlement_date": currency.settlement_date.strftime("%m/%d/%Y")
                if currency.settlement_date is not None
                else "N/A",
                "settlement_date_swap": currency.settlement_date,
            }

            currency_type = currency.currency_ticker_name.type
        return render(
            request,
            "app_exchanges/currencies/currency_prices.html",
            context={
                "current_ticker": current_ticker,
                "ticker_descr": ticker_descr,
                "ticker": ticker,
                "currency_type": currency_type,
            },
        )


def main_view(request, asset_class=None):
    asset_classes = request.GET.getlist(
        "asset_class"
    )  # retrieveing a list of asset classes from the user
    selected_asset_classes = set(
        asset_classes
    )  # retrieveing a list of asset classes from the user
    types = request.GET.getlist("types")  # retrieveing a list of types from the user
    currency_types = set(types)  # retrieveing a list of types from the user

    commodity_exchanges = (
        Exchanges_Commodities.objects.all()
    )  # fetching all commodity tickers from Exchanges_Commodities
    # class
    all_tickers = {}  # creating a dictionary to manipulate our data
    for commodity in commodity_exchanges:  # iterate through objects or retrieved data
        key = (
            1,
            commodity.commodity_ticker_name.id,
        )  # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            "exchange": commodity.exchange.exchange_name,  # storing a name of an exchange
            "asset_class": "Commodity",  # storing a name of our asset class
            "ticker": commodity.commodity_ticker_name.commodity_ticker_name,  # storing a name of the ticker
            "price": commodity.price,  # storing a current price
        }

    currency_exchanges = (
        Exchanges_Currencies.objects.all()
    )  # fetching all commodity tickers from Exchanges_Currencies
    for currency in currency_exchanges:  # iterate through objects or retrieved data
        key = (
            2,
            currency.currency_ticker_name.id,
        )  # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            "exchange": currency.exchange.exchange_name,  # storing a name of an exchange
            "asset_class": "Currency",  # storing a name of our asset class
            "ticker": currency.currency_ticker_name.currency_ticker_name,  # storing a name of the ticker
            "price": currency.price,  #  storing a current price
            "tenor": currency.tenor_months,  # storing Tenor date
            "currency_type": currency.currency_ticker_name.type,  # storing a currency type
        }
    print(all_tickers)
    filtered_tickers = (
        {}
    )  # creating a dictionary to store a filtered on the user's side data

    if "all" in selected_asset_classes or not asset_classes:  #
        filtered_tickers = all_tickers  # if all nothing is chosen - keep the same data
    else:
        for (
            key,
            value,
        ) in (
            all_tickers.items()
        ):  # else - filter by asset classes we received from the user
            if value["asset_class"] in selected_asset_classes:
                filtered_tickers[
                    key
                ] = value  # only add to a dictionary what we have in filters

    if currency_types:
        filtered_tickers = {
            key: value
            for key, value in filtered_tickers.items()
            if "currency_type" in value and value["currency_type"] in currency_types
        }

    currency_types = Currency.objects.values_list(
        "type", flat=True
    ).distinct()  # fetching a list of types from
    # a database

    return render(
        request,
        "main.html",
        context={"all_tickers": filtered_tickers, "currency_types": currency_types},
    )


def admin_dashboard(request):
    currency_form = CurrencyForm()
    if request.method == "POST":
        if "exchange" in request.POST:  # handle a form Add a new exchange
            exchange_form = ExchangeForm(request.POST)  # Initializes
            # the ExchangeForm with the POST data
            if exchange_form.is_valid():  # Validates the form data
                exchange_form.save()  # Saves the form data
                # (creating a new Exchange object in the database).
                return redirect("admin_dashboard")  # Redirects back to the same page
            else:
                print(exchange_form.errors)

        if "commodity" in request.POST:  # handle a form add a new commodity
            commodity_form = CommodityForm(request.POST)
            if commodity_form.is_valid():
                commodity_form.save()
                return redirect("admin_dashboard")
        else:
            commodity_form = CommodityForm()

        if "currency" in request.POST:  # handle a form add a new currency
            currency_form = CurrencyForm(request.POST)
            if currency_form.is_valid():
                currency_form.save()
                return redirect("admin_dashboard")

        if (
            "exchanges_commodities" in request.POST
        ):  # handle a form exchange commodities
            exchanges_commodities_form = ExchangesCommoditiesForm(request.POST)
            if exchanges_commodities_form.is_valid():
                exchanges_commodities_form.save()
                return redirect("admin_dashboard")

    else:
        exchange_form = ExchangeForm()
        commodity_form = CommodityForm()
        currency_form = CurrencyForm()
        exchanges_commodities_form = ExchangesCommoditiesForm()

    exchanges = Exchange.objects.all()
    commodities = Commodity.objects.all()
    currencies = Currency.objects.all()
    return render(
        request,
        "admin_dashboard.html",
        {
            "exchanges": exchanges,
            "exchange_form": exchange_form,
            "commodities": commodities,
            "commodity_form": commodity_form,
            "currencies": currencies,
            "currency_form": currency_form,
            "exchanges_commodities_form": exchanges_commodities_form,
        },
    )


def delete_exchange(request, id):  # method to delete exchanges from the database
    exchange = Exchange.objects.get(
        id=id
    )  # fetching the exchange object with the given id from the database
    exchange.delete()  # deleting the fetched Exchange object from the database.
    return redirect("admin_dashboard")


def delete_commodity(request, id):  # method to delete commodities
    commodity = Commodity.objects.get(id=id)
    commodity.delete()
    return redirect("admin_dashboard")


def delete_currency(request, id):  # methos to delete currency
    currency = Currency.objects.get(id=id)
    currency.delete()
    return redirect("admin_dashboard")


def page_not_found_view(request, exception):
    return render(request, "app_exchanges/base.html")

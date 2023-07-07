from django.shortcuts import render
from django.contrib import messages
from .models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from .forms import (
    CommodityForm, ExchangeForm, CurrencyForm, ExchangesCommoditiesForm, ExchangesCurrenciesForm
)
from app_exchanges.helper_functions.filters_helper import get_all_tickers, filter_tickers, asset_class_view_filter
from app_exchanges.helper_functions.forms_helper import (
    create_commodity, create_exchanges_commodities, create_exchanges_currencies,
    create_currency_form, create_exchange_form
)

#website main_page with a list of all commodities and exchanges
def main_view(request):
    asset_classes = request.GET.getlist('asset_class') #retrieveing a list of asset classes from the user
    selected_asset_classes = set(asset_classes) #converting a retrieved list to a set
    types = request.GET.getlist('types')  #retrieveing a list of currency types from the user
    currency_types = set(types)  #converting a retrieved list of types to a set
    all_tickers = get_all_tickers() #calling the function to retrieve data
    filtered_tickers = filter_tickers(all_tickers, selected_asset_classes, currency_types) #calling the function
    #to filter data
    currency_types_database = Currency.objects.values_list('type', flat=True).distinct() # fetching a list of types
    # from our database
    return render(request, 'main.html', context={'all_tickers': filtered_tickers,
                                                 'currency_types': currency_types_database})



# function to view specific ticker and places to buy}
def asset_class_view(request, asset_class, ticker, id_ticker_id):
    ticker_descr = '' # declare a variable to save a ticker descr
    current_ticker = asset_class_view_filter(asset_class, ticker, id_ticker_id) #calling the function to
    #to retrieve this ticker's data
    if asset_class == 'commodity':

        return render(request, 'app_exchanges/commodities/commodity_prices.html',
                      context={'current_ticker': current_ticker,
                               'ticker_descr': ticker_descr,
                               'ticker': ticker})

    else:

        current_ticker, currency_type = asset_class_view_filter(asset_class, ticker, id_ticker_id)
        return render(request, 'app_exchanges/currencies/currency_prices.html',
                      context={'current_ticker': current_ticker,
                               'ticker_descr': ticker_descr,
                               'ticker': ticker,
                               "currency_type": currency_type
                               })

#admin_dashboard web-page
def admin_dashboard(request):
    exchange_form = ExchangeForm() #creates an instance of the ExchangeForm form class
    commodity_form = CommodityForm() #creates an instance of the CommodityForm form class
    currency_form = CurrencyForm() #creates an instance of the CurrencyForm form class
    exchanges_commodities_form = ExchangesCommoditiesForm() #creates an instance of the
    # exchangesCommoditiesForm class
    exchanges_currencies_form = ExchangesCurrenciesForm() #creates an instance of the
    # exchanges_currencies_form class

    if request.method == "POST":
        if 'commodity' in request.POST:
            commodity_form = CommodityForm(request.POST) #  data submitted via form
            create_commodity(request, commodity_form) #calling a helper function to take of form

        elif 'exchanges_commodities' in request.POST:
            exchanges_commodities_form = ExchangesCommoditiesForm(request.POST)#  data submitted via form
            create_exchanges_commodities(request, exchanges_commodities_form)

        elif 'exchanges_currencies' in request.POST:
            exchanges_currencies_form = ExchangesCurrenciesForm(request.POST)#  data submitted via form
            create_exchanges_currencies(request, exchanges_currencies_form)

        elif 'currency' in request.POST:
            currency_form = CurrencyForm(request.POST)#  data submitted via form
            create_currency_form(request, currency_form)

        elif 'exchange' in request.POST:#  data submitted via form
            exchange_form = ExchangeForm(request.POST)
            create_exchange_form(request, exchange_form)

    exchanges = Exchange.objects.all()
    commodities = Commodity.objects.all()
    currencies = Currency.objects.all()
    exchanges_commodities = Exchanges_Commodities.objects.all()
    exchanges_currencies = Exchanges_Currencies.objects.all()

    return render(request, 'admin_dashboard.html', {
        'exchanges': exchanges,
        'exchange_form': exchange_form,
        'commodities': commodities,
        'commodity_form': commodity_form,
        'currencies': currencies,
        'currency_form': currency_form,
        'exchanges_commodities_form': exchanges_commodities_form,
        'exchanges_currencies_form': exchanges_currencies_form,
        'messages': messages.get_messages(request),
        'exchanges_commodities': exchanges_commodities,
        'exchanges_currencies': exchanges_currencies
    })



def page_not_found_view(request, exception):
    return render(request, 'main.html')

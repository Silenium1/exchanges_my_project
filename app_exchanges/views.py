from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from django.db.models import Q
from .forms import CommodityForm, ExchangeForm, CurrencyForm, ExchangesCommoditiesForm, ExchangesCurrenciesForm
from django.core.exceptions import ValidationError
asset_classes = {"commodity", 'currency'}

#website main_page with a list of all commodities and exchanges. Render main.html
def main_view(request):
    asset_classes = request.GET.getlist('asset_class') #retrieveing a list of asset classes from the user
    selected_asset_classes = set(asset_classes) #retrieveing a list of asset classes from the user
    types = request.GET.getlist('types')  #retrieveing a list of types from the user
    currency_types = set(types) #retrieveing a list of types from the user

    commodity_exchanges = Exchanges_Commodities.objects.all() #fetching all commodity tickers from Exchanges_Commodities
    #class
    all_tickers = {} #creating a dictionary to manipulate our data
    for commodity in commodity_exchanges: # iterate through objects or retrieved data
        key = (1, commodity.commodity_ticker_name.id) # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            'exchange': commodity.exchange.exchange_name, # storing a name of an exchange
            'asset_class': 'Commodity', #storing a name of our asset class
            'ticker': commodity.commodity_ticker_name.commodity_ticker_name, # storing a name of the ticker
            'price': commodity.price, # storing a current price
        }

    currency_exchanges = Exchanges_Currencies.objects.all()   #fetching all commodity tickers from Exchanges_Currencies
    for currency in currency_exchanges: # iterate through objects or retrieved data
        key = (2, currency.currency_ticker_name.id) # hashmap key in the format (Asset class ID, Commodity ID)
        all_tickers[key] = {
            'exchange': currency.exchange.exchange_name, # storing a name of an exchange
            'asset_class': 'Currency', #storing a name of our asset class
            'ticker': currency.currency_ticker_name.currency_ticker_name, # storing a name of the ticker
            'price': currency.price, #  storing a current price
            'tenor': currency.tenor_months,  # storing Tenor date
            'currency_type': currency.currency_ticker_name.type  #storing a currency type
        }

    filtered_tickers = {} # creating a dictionary to store a filtered on the user's side data

    if "all" in selected_asset_classes or not asset_classes: #
        filtered_tickers = all_tickers # if all nothing is chosen - keep the same data
    else:
        for key, value in all_tickers.items(): # else - filter by asset classes we received from the user
            if value['asset_class'] in selected_asset_classes:
                filtered_tickers[key] = value # only add to a dictionary what we have in filters

    if currency_types: #filter by currency type
        filtered_tickers = {
            key: value for key, value in filtered_tickers.items()
            if 'currency_type' in value and value['currency_type'] in currency_types
        }

    currency_types = Currency.objects.values_list('type', flat=True).distinct() # fetching a list of types from
    #a database


    return render(request, 'main.html', context={'all_tickers': filtered_tickers, 'currency_types': currency_types})
    #rendering main.html. Passing our dictionry to a template




# function to view specific ticker and places to buy}
def asset_class_view(request, asset_class, ticker, id_ticker_id):
    current_ticker = {} # dictionary to store a current ticket info
    currency_type = '' # declare a variable to save a currency type
    ticker_descr = ''
    # currency = Currency.objects.get(id=id_ticker_id)  #fetching currency data with the current ticker ID
    # currency_type = currency.type # getting a current currency type
    if asset_class == 'commodity': #commodity render
        commodity_exchanges = Exchanges_Commodities.objects.filter(commodity_ticker_name__id=id_ticker_id)
        # fetching a commodity ticker with this ticker id

        for commodity in commodity_exchanges: #iterate through to get all the data for this commodity ticker
            key = (commodity.exchange.id, commodity.commodity_ticker_name.id) #hashmap Exchange ID / commodity ID
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

        return render(request, 'app_exchanges/commodities/commodity_prices.html',
                      context={'current_ticker': current_ticker, 'ticker_descr': ticker_descr, 'ticker': ticker})

    elif asset_class == 'currency': #currency render
        currency_exchanges = Exchanges_Currencies.objects.filter(currency_ticker_name__id=id_ticker_id)
        # fetching a currency ticker with this ticker id
        for currency in currency_exchanges: #iterate through to get all the data for this currency ticker
            key = (currency.exchange_id, currency.currency_ticker_name_id)  #hashmap Exchange ID / currency ID
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

            currency_type = currency.currency_ticker_name.type # get a current ticker currency type
        return render(request, 'app_exchanges/currencies/currency_prices.html',
                      context={'current_ticker': current_ticker, 'ticker_descr': ticker_descr,
                               'ticker': ticker, "currency_type": currency_type
                               })




def admin_dashboard(request):
    exchange_form = ExchangeForm() #ExchangeForm from forms.py saved in variable
    commodity_form = CommodityForm() #CommodityForm from forms.py saved in variable
    currency_form = CurrencyForm() #CurrencyForm from forms.py saved in variable
    exchanges_commodities_form = ExchangesCommoditiesForm()  #ExchangesCommoditiesForm from forms.py saved in variable
    exchanges_currencies_form = ExchangesCurrenciesForm()  #ExchangesCurrenciesForm from forms.py saved in variable


    if request.method == "POST":

        if 'commodity' in request.POST:
            commodity_form = CommodityForm(request.POST)
            if commodity_form.is_valid():
                commodity_ticker_name =  commodity_form.cleaned_data['commodity_ticker_name'] #dictionary-like object that contains the cleaned form data after it has been validated
                commodity_descr = commodity_form.cleaned_data['commodity_descr'] #dictionary-like object that contains the cleaned form data after it has been validated
                if Commodity.objects.filter(Q(commodity_ticker_name=commodity_ticker_name) #duplicate check
                                            | Q(commodity_descr=commodity_descr)).exists():
                    messages.error(request, "Commodity already exists", extra_tags='red') #message notification
                    #in case this entry already exists
                else:
                    try:
                        commodity_form.save() # save data to our database
                        messages.success(request, "Commodity successfully created!")
                        return redirect('admin_dashboard') #redirect to the main page
                    except ValidationError as e:
                        messages.error(request, f"Failed to create commodity: {e}")


            else:
                print(f"Commodity form errors: {commodity_form.errors}")




        elif 'exchanges_commodities' in request.POST:
            exchanges_commodities_form = ExchangesCommoditiesForm(request.POST)
            if exchanges_commodities_form.is_valid():
                exchange = exchanges_commodities_form.cleaned_data['exchange'] #dictionary-like object that contains the cleaned form data after it has been validated
                commodity_ticker_name = exchanges_commodities_form.cleaned_data['commodity_ticker_name'] #dictionary-like object that contains the cleaned form data after it has been validated
                if Exchanges_Commodities.objects.filter(Q(exchange=exchange) # duplicate check
                                                        & Q(commodity_ticker_name=commodity_ticker_name)).exists():
                    messages.error(request, "Commodity ticker already exists", extra_tags='red')
                else:
                    try:
                        exchanges_commodities_form.save() # save data to our database
                        messages.success(request, "Exchanges commodities successfully created!")
                        return redirect('admin_dashboard')
                    except ValidationError as e: #block is used to catch any ValidationError that may occur during the attempt to save the form data
                        messages.error(request, f"Failed to create a new commodity ticker {e}")



                return redirect('admin_dashboard')
            else:
                print(f"Exchanges commodities form errors: {exchanges_commodities_form.errors}")


        elif 'exchanges_currencies' in request.POST:
            exchanges_currencies_form = ExchangesCurrenciesForm(request.POST)
            if exchanges_currencies_form.is_valid():
                exchange = exchanges_currencies_form.cleaned_data['exchange'] #dictionary-like object that contains the cleaned form data after it has been validated
                currency_ticker_name = exchanges_currencies_form.cleaned_data['currency_ticker_name'] #dictionary-like object that contains the cleaned form data after it has been validated
                if Exchanges_Currencies.objects.filter(Q(exchange=exchange) # duplicate check
                                                        & Q(currency_ticker_name=currency_ticker_name)).exists():
                    messages.error(request, "Currency ticker already exists", extra_tags='red')
                else:
                    try:
                        exchanges_currencies_form.save() # save data to our database
                        messages.success(request, "Exchanges currencies successfully created!")
                        return redirect('admin_dashboard')
                    except ValidationError as e:
                        messages.error(request, f"Failed to create a new currency ticker {e}")

            else:
                print(f"Exchanges currencies form errors: {exchanges_currencies_form.errors}")



        elif 'currency' in request.POST:

            currency_form = CurrencyForm(request.POST)
            if currency_form.is_valid():
                currency_ticker_name = currency_form.cleaned_data['currency_ticker_name'] #dictionary-like object that contains the cleaned form data after it has been validated
                if Currency.objects.filter(currency_ticker_name=currency_ticker_name).exists(): #duplicate check
                    messages.error(request, "Currency already exists.", extra_tags='red')

                else:
                    try:
                        currency_form.save() # save data to our database
                        messages.success(request, "Currency successfully created!")
                        return redirect('admin_dashboard')

                    except ValidationError as e:
                        messages.error(request, f"Failed to create currency: {e}")

            else:
                print(f"Currency form errors: {currency_form.errors}")



        elif 'exchange' in request.POST:
            exchange_form = ExchangeForm(request.POST)
            if exchange_form.is_valid():
                exchange_abbr = exchange_form.cleaned_data['exchange_abbr'] #dictionary-like object that contains the cleaned form data after it has been validated
                exchange_name = exchange_form.cleaned_data['exchange_name'] #dictionary-like object that contains the cleaned form data after it has been validated
                if Exchange.objects.filter(Q(exchange_abbr=exchange_abbr) | Q(exchange_name=exchange_name)).exists(): #duplicate check
                    messages.error(request, "Exchange already exists.", extra_tags='red')

                else:
                    try:
                        exchange_form.save() # save data to our database
                        messages.success(request, "Exchange successfully created!")
                        return redirect('admin_dashboard')

                    except ValidationError as e:
                        messages.error(request, f"Failed to create exchange: {e}")

            else:
                print(f"Exchange form errors: {exchange_form.errors}")

    exchanges = Exchange.objects.all() #retrieving all the objects
    commodities = Commodity.objects.all()  #retrieving all the objects
    currencies = Currency.objects.all()  #retrieving all the objects
    exchanges_commodities = Exchanges_Commodities.objects.all()  #retrieving all the objects
    exchanges_currencies = Exchanges_Currencies.objects.all()  #retrieving all the objects
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



def delete_exchange(request, id): #method to delete exchanges from the database
    exchange = Exchange.objects.get(id=id) #fetching the exchange object with the given id from the database
    exchange.delete() # deleting the fetched Exchange object from the database.
    return redirect('admin_dashboard')

def delete_commodity(request, id): #method to delete commodities
    commodity = Commodity.objects.get(id=id)
    commodity.delete()
    return redirect('admin_dashboard')

def delete_currency(request, id): #method to delete currency
    currency = Currency.objects.get(id=id)
    currency.delete()
    return redirect('admin_dashboard')


def delete_exchanges_commodities(request, id):  #method to delete exchange commodities
    exchange_commodity = Exchanges_Commodities.objects.get(id=id)
    exchange_commodity.delete()
    return redirect('admin_dashboard')


def delete_exchanges_currencies(request, id): #method to delete currency commodities
    exchange_currency = Exchanges_Currencies.objects.get(id=id)
    exchange_currency.delete()
    return redirect('admin_dashboard')
def page_not_found_view(request, exception):
    return render(request, 'app_exchanges/base.html')

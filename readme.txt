on my main.html I have filters made using html and css

{% load static %}

<html>
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Exchanges report">
    <title>Exchanges report</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{% static 'app_exchanges/css/main.css' %}">
    <style>
        /* Add custom styles for the checkbox list */
        .checkbox-list {
            list-style-type: none;
            padding: 0;
        }
        .checkbox-list li {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <a class="top-right-link" href="{% url 'admin_dashboard' %}">Go to Admin Dashboard</a>{# link to the admin dashboard #}
    <div class="container">
        <div class="sidebar1"> {# link to the admin dashboard #}
            <h2>Logo</h2>
            <form id="filter-form" method="GET" action="{% url 'main_view' %}">
                <h3>Main Filters</h3>
                <ul class="checkbox-list"> {# checkboxes for asset classes #}
                    <li>
                        <strong>Asset class</strong>
                    </li>
                    <li>
                        <label class="checkbox-label">
                            <input type="checkbox" name="asset_class" value="all">{# checkbox for all #}
                            All Asset Classes
                        </label>
                    </li>
                    <li>
                        <label class="checkbox-label">
                            <input type="checkbox" name="asset_class" value="Commodity">{# checkbox for commodity #}
                            Commodity
                        </label>
                    </li>
                    <li>
                        <label class="checkbox-label">
                            <input type="checkbox" name="asset_class" value="Currency">{# checkbox for currency #}
                            Currency
                        </label>
                    </li>
                </ul>
                <h3>Currency filters</h3>
                <ul class="checkbox-list">
                    <li>
                        <strong>Currency Type</strong>
                    </li>
                    {% for type in currency_types %}
                    <li>
                        <label class="checkbox-label">
                            <input type="checkbox" name="types" value="{{ type }}">  {# checkbox for each currency type #}
                            {{ type }}
                        </label>
                    </li>
                    {% endfor %}
                </ul>
                <button type="submit">Apply Filters</button>
                <button type="reset" onclick="location.href='{{ request.path }}'">Reset Filters</button> <!-- Updated button with onclick event -->
            </form>
        </div>
        <div class="content">
            <h1>Exchanges Report</h1>
            <table>
                <thead>
                    <tr>
                        <th>Asset class</th>
                        <th class="fixed-width">Ticker</th>
                        <th>Trade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for ticker, info in all_tickers.items %}
                    <tr class="ticker-row" data-asset-class="{{ info.asset_class }}">
                        <td>{{ info.asset_class }}</td>
                        <td class="fixed-width">{{ info.ticker }}</td>
                        <th>
                            <a href="{% url 'asset_class' info.asset_class|slugify info.ticker|slugify ticker.1 %}">Compare prices</a>
                        </th>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="3">No tickers found.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>


views.py


from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from django.db.models import Q
from .forms import CommodityForm
from .forms import ExchangeForm
from .forms import CurrencyForm
from .forms import ExchangesCommoditiesForm
from .forms import ExchangesCurrenciesForm
from django.core.exceptions import ValidationError
asset_classes = {"commodity", 'currency'}

# def asset_class_redirect(request, asset_class):
#     return redirect('main_view')


def asset_class_view(request, asset_class, ticker, id_ticker_id):
    current_ticker = {} # dictionary to store a current ticket info
    currency_type = '' # declare a variable to save a currency type
    ticker_descr = ''
    # currency = Currency.objects.get(id=id_ticker_id)  #fetching currency data with the current ticker ID
    # currency_type = currency.type # getting a current currency type
    if asset_class == 'commodity':
        commodity_exchanges = Exchanges_Commodities.objects.filter(commodity_ticker_name__id=id_ticker_id)
        # fetchinG a currency ticker with this ticker id

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

    elif asset_class == 'currency':
        currency_exchanges = Exchanges_Currencies.objects.filter(currency_ticker_name__id=id_ticker_id)

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

            currency_type = currency.currency_ticker_name.type
        return render(request, 'app_exchanges/currencies/currency_prices.html',
                      context={'current_ticker': current_ticker, 'ticker_descr': ticker_descr,
                               'ticker': ticker, "currency_type": currency_type
                               })





def main_view(request, asset_class=None):  #main_page
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
    print(all_tickers)
    filtered_tickers = {} # creating a dictionary to store a filtered on the user's side data

    if "all" in selected_asset_classes or not asset_classes: #
        filtered_tickers = all_tickers # if all nothing is chosen - keep the same data
    else:
        for key, value in all_tickers.items(): # else - filter by asset classes we received from the user
            if value['asset_class'] in selected_asset_classes:
                filtered_tickers[key] = value # only add to a dictionary what we have in filters

    if currency_types:
        filtered_tickers = {
            key: value for key, value in filtered_tickers.items()
            if 'currency_type' in value and value['currency_type'] in currency_types
        }

    currency_types = Currency.objects.values_list('type', flat=True).distinct() # fetching a list of types from
    #a database

    return render(request, 'main.html', context={'all_tickers': filtered_tickers, 'currency_types': currency_types})


def admin_dashboard(request):
    exchange_form = ExchangeForm()
    commodity_form = CommodityForm()
    currency_form = CurrencyForm()
    exchanges_commodities_form = ExchangesCommoditiesForm()
    exchanges_currencies_form = ExchangesCurrenciesForm()


    if request.method == "POST":

        if 'commodity' in request.POST:
            commodity_form = CommodityForm(request.POST)
            if commodity_form.is_valid():
                commodity_ticker_name =  commodity_form.cleaned_data['commodity_ticker_name']
                commodity_descr = commodity_form.cleaned_data['commodity_descr']
                if Commodity.objects.filter(Q(commodity_ticker_name=commodity_ticker_name)
                                            | Q(commodity_descr=commodity_descr)).exists():
                    messages.error(request, "Commodity already exists", extra_tags='red')
                else:
                    try:
                        commodity_form.save()
                        messages.success(request, "Commodity successfully created!")
                        return redirect('admin_dashboard')
                    except ValidationError as e:
                        messages.error(request, f"Failed to create commodity: {e}")


            else:
                print(f"Commodity form errors: {commodity_form.errors}")




        elif 'exchanges_commodities' in request.POST:
            exchanges_commodities_form = ExchangesCommoditiesForm(request.POST)
            if exchanges_commodities_form.is_valid():
                exchange = exchanges_commodities_form.cleaned_data['exchange']
                commodity_ticker_name = exchanges_commodities_form.cleaned_data['commodity_ticker_name']
                if Exchanges_Commodities.objects.filter(Q(exchange=exchange)
                                                        & Q(commodity_ticker_name=commodity_ticker_name)).exists():
                    messages.error(request, "Commodity ticker already exists", extra_tags='red')
                else:
                    try:
                        exchanges_commodities_form.save()
                        messages.success(request, "Exchanges commodities successfully created!")
                        return redirect('admin_dashboard')
                    except ValidationError as e:
                        messages.error(request, f"Failed to create a new commodity ticker {e}")



                return redirect('admin_dashboard')
            else:
                print(f"Exchanges commodities form errors: {exchanges_commodities_form.errors}")


        elif 'exchanges_currencies' in request.POST:
            exchanges_currencies_form = ExchangesCurrenciesForm(request.POST)
            if exchanges_currencies_form.is_valid():
                exchange = exchanges_currencies_form.cleaned_data['exchange']
                currency_ticker_name = exchanges_currencies_form.cleaned_data['currency_ticker_name']
                if Exchanges_Currencies.objects.filter(Q(exchange=exchange)
                                                        & Q(currency_ticker_name=currency_ticker_name)).exists():
                    messages.error(request, "Currency ticker already exists", extra_tags='red')
                else:
                    try:
                        exchanges_currencies_form.save()
                        messages.success(request, "Exchanges currencies successfully created!")
                        return redirect('admin_dashboard')
                    except ValidationError as e:
                        messages.error(request, f"Failed to create a new currency ticker {e}")

            else:
                print(f"Exchanges currencies form errors: {exchanges_currencies_form.errors}")



        elif 'currency' in request.POST:

            currency_form = CurrencyForm(request.POST)
            if currency_form.is_valid():
                currency_ticker_name = currency_form.cleaned_data['currency_ticker_name']
                if Currency.objects.filter(currency_ticker_name=currency_ticker_name).exists():
                    messages.error(request, "Currency already exists.", extra_tags='red')

                else:
                    try:
                        currency_form.save()
                        messages.success(request, "Currency successfully created!")
                        return redirect('admin_dashboard')

                    except ValidationError as e:
                        messages.error(request, f"Failed to create currency: {e}")

            else:
                print(f"Currency form errors: {currency_form.errors}")



        elif 'exchange' in request.POST:
            exchange_form = ExchangeForm(request.POST)
            if exchange_form.is_valid():
                exchange_abbr = exchange_form.cleaned_data['exchange_abbr']
                exchange_name = exchange_form.cleaned_data['exchange_name']
                if Exchange.objects.filter(Q(exchange_abbr=exchange_abbr) | Q(exchange_name=exchange_name)).exists():
                    messages.error(request, "Exchange already exists.", extra_tags='red')

                else:
                    try:
                        exchange_form.save()
                        messages.success(request, "Exchange successfully created!")
                        return redirect('admin_dashboard')

                    except ValidationError as e:
                        messages.error(request, f"Failed to create exchange: {e}")

            else:
                print(f"Exchange form errors: {exchange_form.errors}")

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



def delete_exchange(request, id): #method to delete exchanges from the database
    exchange = Exchange.objects.get(id=id) #fetching the exchange object with the given id from the database
    exchange.delete() # deleting the fetched Exchange object from the database.
    return redirect('admin_dashboard')

def delete_commodity(request, id): #method to delete commodities
    commodity = Commodity.objects.get(id=id)
    commodity.delete()
    return redirect('admin_dashboard')

def delete_currency(request, id): #methos to delete currency
    currency = Currency.objects.get(id=id)
    currency.delete()
    return redirect('admin_dashboard')


def delete_exchanges_commodities(request, id):
    exchange_commodity = Exchanges_Commodities.objects.get(id=id)
    exchange_commodity.delete()
    return redirect('admin_dashboard')


def delete_exchanges_currencies(request, id):
    exchange_currency = Exchanges_Currencies.objects.get(id=id)
    exchange_currency.delete()
    return redirect('admin_dashboard')
def page_not_found_view(request, exception):
    return render(request, 'app_exchanges/base.html')


on this html page, I need to replace all JS scripts with the same html ones

{% load static %}

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Your page description here">
    <meta name="keywords" content="your, keywords, here">
    <meta name="author" content="Your Name">
    <title>Exchanges Report</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="{% static 'app_exchanges/css/compare_prices.css' %}">
</head>
<body>
    <div class="container">
        <div class="sidebar2">
            <h2>Choose your exchange</h2>
            <form id="filter-form" method="GET">
                <ul>
                    <li>
                        <input type="checkbox" id="all" name="exchange" value="all" onclick="selectAllExchanges(this);">
                        <label for="all">All Exchanges</label>
                    </li>
                    {% for value in current_ticker.values %}
                        <li>
                            <input type="checkbox" id="{{ value.exchange }}" name="exchange" value="{{ value.exchange }}" onclick="filterTable('{{ value.exchange }}', this);">
                            <label for="{{ value.exchange }}">{{ value.exchange }}</label>
                        </li>
                    {% endfor %}
                </ul>
            </form>
        </div>
        <div class="content">
            <h1>{{ ticker }}</h1>
           <h2>{{ ticker_descr }}</h2>

            <table>
                <thead>
                    <tr>
                        <th>Exchange</th>
                        <th>Unit</th>
                        <th>Price</th>
                        <th>Time of last trade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for key, value in current_ticker.items %}
                        <tr class="{{ value.exchange }}">
                            <td>{{ value.exchange }}</td>
                            <td>{{ value.unit_int_value }} {{ value.unit_str_value }}</td>
                            <td>{{ value.price }} $</td>
                            <td>{{ value.time_of_last_trade }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
             </table>
             <p class="main-page-link">
                <a href="{% url 'main_view' %}">Go to Main Page</a>
            </p>
        </div>
    </div>



    <script>
        // Load any saved checkbox states from local storage
        window.onload = function() {
            const checkboxes = document.querySelectorAll('#filter-form input[type=checkbox]');
            checkboxes.forEach(function(checkbox) {
                const checkboxState = localStorage.getItem(checkbox.id);
                if (checkboxState === 'true') {
                    checkbox.checked = true;
                }
            });
            filterTable();
        };

        function updateCheckboxState(checkbox) {
            localStorage.setItem(checkbox.id, checkbox.checked);
            filterTable();
        }

        function selectAllExchanges(checkbox) {
            const exchangeCheckboxes = document.getElementsByName('exchange');
            for (let i = 0; i < exchangeCheckboxes.length; i++) {
                exchangeCheckboxes[i].checked = checkbox.checked;
                updateCheckboxState(exchangeCheckboxes[i]);
            }
            filterTable();
        }

        function filterTable() {
            const exchangeCheckboxes = document.getElementsByName('exchange');
            const exchangeTable = document.querySelector('table');
            const rows = exchangeTable.getElementsByTagName('tr');
            let isAnyCheckboxChecked = false;

            for (let i = 0; i < exchangeCheckboxes.length; i++) {
                if (exchangeCheckboxes[i].checked) {
                    isAnyCheckboxChecked = true;
                    break;
                }
            }

            for (let i = 1; i < rows.length; i++) {
                const exchangeName = rows[i].getAttribute('class');
                let shouldDisplay = false;
                if (exchangeName) {
                    if (isAnyCheckboxChecked) {
                        for (let j = 0; j < exchangeCheckboxes.length; j++) {
                            if (exchangeCheckboxes[j].checked && exchangeCheckboxes[j].value === exchangeName) {
                                shouldDisplay = true;
                                break;
                            }
                        }
                    } else {
                        shouldDisplay = true; // Display all rows when no checkboxes are checked
                    }
                } else {
                    shouldDisplay = true; // Display rows without class (table header)
                }
                rows[i].style.display = shouldDisplay ? '' : 'none';
            }
        }
    </script>
</body>
</html>




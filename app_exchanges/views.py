from django.shortcuts import render
from django.http import Http404
from django.db.models import F
from django.shortcuts import redirect
from .models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from django.db.models.functions import Lower
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommodityForm


asset_classes = {"commodity", 'currency'}

# def asset_class_redirect(request, asset_class):
#     return redirect('main_view')


def asset_class_view(request, asset_class, ticker, id_ticker_id):
    current_ticker = {}
    ticker_descr = ''
    currency = Currency.objects.get(id=id_ticker_id)
    currency_type = currency.type
    print(currency_type)
    if asset_class == 'commodity':
        commodity_exchanges = Exchanges_Commodities.objects.filter(commodity_ticker_name__id=id_ticker_id)

        for commodity in commodity_exchanges:
            print(commodity)
            key = (commodity.exchange.id, commodity.commodity_ticker_name.id)
            print(key)
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
            if not ticker_descr:
                ticker_descr = commodity.commodity_ticker_name.commodity_descr
        print(current_ticker)
        return render(request, 'app_exchanges/commodities/commodity_prices.html',
                      context={'current_ticker': current_ticker, 'ticker_descr': ticker_descr, 'ticker': ticker})

    elif asset_class == 'currency':
        currency_exchanges = Exchanges_Currencies.objects.filter(currency_ticker_name__id=id_ticker_id)

        for currency in currency_exchanges:
            key = (currency.exchange_id, currency.currency_ticker_name_id)
            current_ticker[key] = {
                'exchange': currency.exchange.exchange_name,
                'asset_class': 'currency',
                'ticker': currency.currency_ticker_name.currency_ticker_name,
                'price': currency.price,
                'tenor': currency.tenor_months,
                'ticker_descr': currency.currency_ticker_name.currency_descr,
                'settlement_date': currency.settlement_date.strftime('%m/%d/%Y') if currency.settlement_date is not None else 'N/A',
                'settlement_date_swap': currency.settlement_date

            }
            if not ticker_descr:
                ticker_descr = currency.currency_ticker_name.currency_descr
        print(current_ticker)
        return render(request, 'app_exchanges/currencies/currency_prices.html',
                      context={'current_ticker': current_ticker, 'ticker_descr': ticker_descr,
                               'ticker': ticker, "currency_type": currency_type
                               })


def main_view(request, asset_class=None):
    asset_classes = request.GET.getlist('asset_class')  # getting asset classes data
    selected_asset_classes = set(asset_classes)  # getting asset classes data

    commodity_exchanges = Exchanges_Commodities.objects.all()
    all_tickers = {}
    for commodity in commodity_exchanges:
        key = (1, commodity.commodity_ticker_name.id)
        all_tickers[key] = {
            'exchange': commodity.exchange.exchange_name,
            'asset_class': 'Commodity',
            'ticker': commodity.commodity_ticker_name.commodity_ticker_name,
            'price': commodity.price,
        }
    currency_exchanges = Exchanges_Currencies.objects.all()
    for currency in currency_exchanges:
        key = (2, currency.currency_ticker_name.id)
        all_tickers[key] = {
            'exchange': currency.exchange.exchange_name,
            'asset_class': 'Currency',
            'ticker': currency.currency_ticker_name.currency_ticker_name,
            'price': currency.price,
            'tenor': currency.tenor_months
        }

    filtered_tickers = {}

    if "all" in selected_asset_classes or not asset_classes:
        filtered_tickers = all_tickers
    else:
        for key, value in all_tickers.items():
            if value['asset_class'] in selected_asset_classes:
                filtered_tickers[key] = value


    print(filtered_tickers)
    return render(request, 'main.html', context={'all_tickers': filtered_tickers})


@staff_member_required
def commodity_view(request):
    if request.method == 'POST':
        form = CommodityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('commodity_list') # you'll have to create this view
    else:
        form = CommodityForm()
    return render(request, 'admin_dashboard.html', {'form': form})



def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
def page_not_found_view(request, exception):
    return render(request, 'app_exchanges/base.html')

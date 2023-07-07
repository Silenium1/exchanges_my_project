
from app_exchanges.models import Exchange, Commodity, Currency, Exchanges_Commodities, Exchanges_Currencies
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render



def create_commodity(request, commodity_form):
    if commodity_form.is_valid(): # # Check if the form data is valid
        # Extract cleaned data
        commodity_ticker_name =  commodity_form.cleaned_data['commodity_ticker_name']
        commodity_descr = commodity_form.cleaned_data['commodity_descr']

        # Check if a commodity with the same ticker name or description already exists
        if Commodity.objects.filter(Q(commodity_ticker_name=commodity_ticker_name)
                                    | Q(commodity_descr=commodity_descr)).exists():
            messages.error(request, "Commodity already exists", extra_tags='red')

        else:
            try:
                # Save the commodity form data to the database
                commodity_form.save()
                # Display a success message after successfully creating the commodity
                messages.success(request, "Commodity successfully created!")
                # Redirect the user back to the admin dashboard
                return redirect('admin_dashboard')
            except ValidationError as e:
                # Display an error message if there was a validation error while saving the commodity
                messages.error(request, f"Failed to create commodity: {e}")
    else:
        # Display form errors if the form data is not valid
        print(f"Commodity form errors: {commodity_form.errors}")




def create_exchanges_commodities(request, exchanges_commodities_form):
    if exchanges_commodities_form.is_valid(): # # Check if the form data is valid

        # Extract cleaned data
        exchange = exchanges_commodities_form.cleaned_data['exchange']
        commodity_ticker_name = exchanges_commodities_form.cleaned_data['commodity_ticker_name']

        # Check if the combination of exchange and commodity ticker already exists
        if Exchanges_Commodities.objects.filter(Q(exchange=exchange)
                                                & Q(commodity_ticker_name=commodity_ticker_name)).exists():
            messages.error(request, "Commodity ticker already exists", extra_tags='red')
            # Display an error message if the combination already exists
        else:
            try:
                # Save the exchanges_commodities form data to the database
                exchanges_commodities_form.save()
                # Display a success message after successfully creating exchanges_commodities
                messages.success(request, "Exchanges commodities successfully created!")
                return redirect('admin_dashboard')
            except ValidationError as e:
                # Display an error message if there was a validation error while saving the exchanges_commodities
                messages.error(request, f"Failed to create a new commodity ticker {e}")
    else:
        # Display form errors if the form data is not valid
        print(f"Exchanges commodities form errors: {exchanges_commodities_form.errors}")




def create_exchanges_currencies(request, exchanges_currencies_form):
    # Check if the form data is valid
    if exchanges_currencies_form.is_valid():
        # Extract cleaned data
        exchange = exchanges_currencies_form.cleaned_data['exchange']
        currency_ticker_name = exchanges_currencies_form.cleaned_data['currency_ticker_name']

        # Check if the combination of exchange and currency ticker already exists
        if Exchanges_Currencies.objects.filter(Q(exchange=exchange)
                                               & Q(currency_ticker_name=currency_ticker_name)).exists():
            # Display an error message if the combination already exists
            messages.error(request, "Currency ticker already exists", extra_tags='red')
        else:
            try:
                # Save the exchanges_currencies form data to the database
                exchanges_currencies_form.save()
                # Display a success message after successfully creating exchanges_currencies
                messages.success(request, "Exchanges currencies successfully created!")
                # Redirect the user back to the admin dashboard
                return redirect('admin_dashboard')
            except ValidationError as e:
                # Display an error message if there was a validation error while saving the exchanges_currencies
                messages.error(request, f"Failed to create a new currency ticker {e}")

    else:
        # Display form errors if the form data is not valid
        print(f"Exchanges currencies form errors: {exchanges_currencies_form.errors}")




def create_currency_form(request, currency_form):
    # Check if the form data is valid
    if currency_form.is_valid():
        # Extract cleaned data
        currency_ticker_name = currency_form.cleaned_data['currency_ticker_name']

        # Check if a currency with the same ticker name already exists
        if Currency.objects.filter(currency_ticker_name=currency_ticker_name).exists():
            # Display an error message if the currency already exists
            messages.error(request, "Currency already exists.", extra_tags='red')

        else:
            try:
                # Save the currency form data to the database
                currency_form.save()
                # Display a success message after successfully creating the currency
                messages.success(request, "Currency successfully created!")
                # Redirect the user back to the admin dashboard
                return redirect('admin_dashboard')

            except ValidationError as e:
                # Display an error message if there was a validation error while saving the currency
                messages.error(request, f"Failed to create currency: {e}")

    else:
        # Display form errors if the form data is not valid
        print(f"Currency form errors: {currency_form.errors}")




def create_exchange_form(request, exchange_form):
    # Check if the form data is valid
    if exchange_form.is_valid():

        # Extract cleaned data
        exchange_abbr = exchange_form.cleaned_data['exchange_abbr']
        exchange_name = exchange_form.cleaned_data['exchange_name']

        # Check if an exchange with the same abbreviation or name already exists
        if Exchange.objects.filter(
                Q(exchange_abbr=exchange_abbr) | Q(exchange_name=exchange_name)).exists():
            messages.error(request, "Exchange already exists.", extra_tags='red')

        else:
            try:
                # Save the exchange form data to the database
                exchange_form.save()
                # Display a success message after successfully creating the exchange
                messages.success(request, "Exchange successfully created!")
                # Redirect the user back to the admin dashboard
                return redirect('admin_dashboard')

            except ValidationError as e:
                # Display an error message if there was a validation error while saving the exchange
                messages.error(request, f"Failed to create exchange: {e}")

    else:
        # Display form errors if the form data is not valid
        print(f"Exchange form errors: {exchange_form.errors}")

    # Render the admin dashboard template
    return render(request, 'admin_dashboard.html')



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
from django.contrib import admin
from .models import (
    Exchange,
    Commodity,
    Currency,
    Exchanges_Commodities,
    Exchanges_Currencies,
)
from django.db.models import QuerySet
from .forms import ExchangeForm


class CurrencyAdmin(admin.ModelAdmin):
    pass


class CommodityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Commodity, CommodityAdmin)


class Exchange_commodity_admin(admin.ModelAdmin):
    list_display = [
        "exchange",
        "commodity_ticker_name",
        "commodity_description",
        "unit_int_value",
        "unit_str_value",
        "price",
    ]
    readonly_fields = ["commodity_description", "unit_int_value", "unit_str_value"]

    def commodity_description(self, obj=None):
        if obj and obj.commodity_ticker_name:
            return obj.commodity_ticker_name.commodity_descr
        return None

    def unit_int_value(self, obj=None):
        if obj and obj.commodity_ticker_name:
            return obj.commodity_ticker_name.unit_int_value
        return None

    def unit_str_value(self, obj=None):
        if obj and obj.commodity_ticker_name:
            return obj.commodity_ticker_name.unit_str_value
        return None

    commodity_description.short_description = "Commodity Description"
    unit_int_value.short_description = "Unit Integer Value"
    unit_str_value.short_description = "Unit String Value"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["commodity_ticker_name"].queryset = Commodity.objects.all()
        return form


admin.site.register(Exchanges_Commodities, Exchange_commodity_admin)


class Exchange_currency_admin(admin.ModelAdmin):
    list_display = ["exchange", "currency_ticker_name", "base_currency", "tenor_months"]


admin.site.register(Exchange)


admin.site.register(Exchanges_Currencies, Exchange_currency_admin)

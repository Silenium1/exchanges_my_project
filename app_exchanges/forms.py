
from django import forms
from .models import Commodity

class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ['commodity_ticker_name', 'commodity_descr', 'unit_int_value', 'unit_str_value']

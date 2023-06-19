import django_tables2 as tables
from .models import Exchanges_Commodities, Exchanges_Currencies

class ExchangesTable(tables.Table):
    asset_type = tables.Column(empty_values=())
    ticker = tables.Column(empty_values=())

    def render_asset_type(self, record):
        if isinstance(record, Exchanges_Commodities):
            return 'Commodity'
        else:
            return record.__class__.__name__

    def render_ticker(self, record):
        if isinstance(record, Exchanges_Commodities):
            return record.commodity_ticker_name.commodity_ticker_name
        elif isinstance(record, Exchanges_Currencies):
            return record.currency_ticker_name.currency_ticker_name

    class Meta:
        model = Exchanges_Commodities
        template_name = 'django_tables2/bootstrap.html'
        fields = ('asset_type', 'ticker') # fields to display

from django.urls import path
from .views import main_view
from app_exchanges.helper_functions.forms_helper import delete_currency, delete_exchange, delete_commodity, \
    delete_exchanges_commodities, delete_exchanges_currencies
from .views import asset_class_view,admin_dashboard

urlpatterns = [
    path('', main_view, name='main_view'),
    path('asset-class/<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class_view'),
    path('<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('delete_exchange/<int:id>/', delete_exchange, name='delete_exchange'),
    path('delete_commodity/<int:id>/', delete_commodity, name='delete_commodity'),
    path('delete_currency/<int:id>/', delete_currency, name='delete_currency'),
    path('delete_exchanges_commodities/<int:id>/', delete_exchanges_commodities, name='delete_exchanges_commodities'),
    path('delete_exchanges_currencies/<int:id>/', delete_exchanges_currencies, name='delete_exchanges_currencies')

]
handler404 = 'app_exchanges.views.page_not_found_view'

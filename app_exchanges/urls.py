from django.urls import path, include
from .views import main_view, page_not_found_view, delete_currency
from .views import asset_class_view,admin_dashboard, delete_exchange, delete_commodity

urlpatterns = [
    path('', main_view, name='main_view'),
    # path('<str:asset_class>/', asset_class_redirect, name='asset_class_redirect'),
    path('asset-class/<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class_view'),
    path('<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('delete_exchange/<int:id>/', delete_exchange, name='delete_exchange'),
    path('delete_commodity/<int:id>/', delete_commodity, name='delete_commodity'),
    path('delete_currency/<int:id>/', delete_currency, name='delete_currency')

]
handler404 = 'app_exchanges.views.page_not_found_view'

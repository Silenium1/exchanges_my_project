from django.urls import path, include
from .views import main_view, page_not_found_view, asset_class_view,admin_dashboard

urlpatterns = [
    path('', main_view, name='main_view'),
    # path('<str:asset_class>/', asset_class_redirect, name='asset_class_redirect'),
    path('asset-class/<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class_view'),
    path('<str:asset_class>/<str:ticker>/<int:id_ticker_id>/', asset_class_view, name='asset_class'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard')
]
handler404 = 'app_exchanges.views.page_not_found_view'

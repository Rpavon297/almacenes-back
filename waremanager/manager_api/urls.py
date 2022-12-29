from django.urls import path
from manager_api.views import WarehouseView, ProductsView, StockView, OrderView


urlpatterns = [
    path('warehouse/', WarehouseView.as_view(), name='Warehouse'),
    path('stock/', StockView.as_view(), name='stock'),
    path('order/', OrderView.as_view(), name='order'),
    path('product/', ProductsView.as_view(), name='product'),
]
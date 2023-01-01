from django.urls import path
from manager_api.views import WarehouseView, ProductsView, StockView, OrderView, DefaultWarehouseView


urlpatterns = [
    path('warehouse/', WarehouseView.as_view(), name='Warehouse'),
    path('warehouse/<int:warehouse_id>', WarehouseView.as_view(), name='Warehouse'),
    path('warehouse/default', DefaultWarehouseView.as_view(), name='Warehouse'),
    path('stock/', StockView.as_view(), name='stock'),
    path('order/', OrderView.as_view(), name='order'),
    path('product/', ProductsView.as_view(), name='product'),
    path('product/<int:product_id>', ProductsView.as_view(), name='product'),
]
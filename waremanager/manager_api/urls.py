from django.contrib import admin
from django.urls import path, re_path
from manager_api.views import WarehouseView
from manager_api.constants import API_VERSION



urlpatterns = [
    path('warehouses/', WarehouseView.as_view(), name='Warehouses'),
]
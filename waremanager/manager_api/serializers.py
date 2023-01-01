from rest_framework import serializers
from manager_api.models import Warehouse, Product, Stock, Order


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    warehouse_address = serializers.CharField(source='warehouse.address')
    class Meta:
        model = Stock
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='stock.product.name')
    warehouse_address = serializers.CharField(source='stock.warehouse.address')
    class Meta:
        model = Order
        fields = '__all__'

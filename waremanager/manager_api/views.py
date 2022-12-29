from rest_framework import permissions
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from manager_api.models import Warehouse, Product, Stock, Order
from manager_api.serializers import WarehouseSerializer, ProductSerializer, StockSerializer, OrderSerializer


# TODO payload and query parameters validations
class WarehouseView(APIView):
    error = False
    response = ""

    def get(self, request):
        data = Warehouse.objects
        params = request.GET

        if params.get("address", None):
            data = data.filter(address=params.get("address"))
        if params.get("id", None):
            data = data.filter(id=params.get("id"))

        self.response = WarehouseSerializer(data.all(), many=True).data
        return Response({
            "response": self.response,
            "error": self.error
        })

    def post(self, request):
        warehouse = Warehouse.objects.create(address=request.data.get("address"))
        self.response = WarehouseSerializer(warehouse, many=False).data

        return Response({
            "response": self.response,
            "error": self.error
        })


class ProductsView(APIView):
    error = False
    response = ""

    def get(self, request):
        data = Product.objects
        params = request.GET

        if params.get("name", None):
            data = data.filter(name=params.get("name"))
        if params.get("id", None):
            data = data.filter(id=params.get("id"))

        self.response = ProductSerializer(data.all(), many=True).data
        return Response({
            "response": self.response,
            "error": self.error
        })

    def post(self, request):
        product = Product.objects.create(name=request.data.get("name"))
        self.response = ProductSerializer(product, many=False).data

        return Response({
            "response": self.response,
            "error": self.error
        })


class StockView(APIView):
    error = False
    response = ""

    def get(self, request):
        data = Stock.objects
        params = request.GET

        if params.get("warehouse", None):
            data = data.filter(warehouse=params.get("warehouse"))
        if params.get("product", None):
            data = data.filter(product=params.get("product"))
        if params.get("id", None):
            data = data.filter(id=params.get("id"))

        self.response = StockSerializer(data.all(), many=True).data
        return Response({
            "response": self.response,
            "error": self.error
        })


class OrderView(APIView):
    error = False
    response = ""

    def get(self, request):
        data = Order.objects
        params = request.GET

        if params.get("date", None):
            data = data.filter(date=params.get("date"))
        if params.get("since", None):
            data = data.filter(date__gte=params.get("since"))
        if params.get("until", None):
            data = data.filter(date__lte=params.get("until"))
        if params.get("id", None):
            data = data.filter(id=params.get("id"))

        self.response = OrderSerializer(data.all(), many=True).data
        return Response({
            "response": self.response,
            "error": self.error
        })

    def post(self, request):
        warehouse = Warehouse.objects.get(id=request.data.get("warehouse"))
        product = Product.objects.get(id=request.data.get("product"))
        if not warehouse:
            self.error = True
            self.response = "Warehouse not found"
        elif not product:
            self.error = True
            self.response = "Product not found"
        else:
            stock = Stock.objects.get_or_create(
                warehouse=warehouse,
                product=product,
            )[0]
            if request.data.get("quantity") + stock.available < 0:
                self.error = True
                self.response = "Not enough available stock"
            else:
                stock.available += request.data.get("quantity")
                stock.save()
                order = Order.objects.create(date=datetime.now(),
                                             quantity=request.data.get("quantity"),
                                             stock=stock)

                self.response = OrderSerializer(order, many=False).data

        return Response({
            "response": self.response,
            "error": self.error
        })

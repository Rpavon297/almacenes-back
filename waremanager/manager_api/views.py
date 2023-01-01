from rest_framework import permissions
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from manager_api.models import Warehouse, Product, Stock, Order, Meta
from manager_api.serializers import WarehouseSerializer, ProductSerializer, StockSerializer, OrderSerializer
from manager_api.constants import DEFAULT_WH


# TODO payload and query parameters validations
# TODO error and exceptions
class WarehouseView(APIView):
    error = False
    response = ""

    def get(self, request, id=None):
        data = Warehouse.objects
        params = request.GET

        if id:
            self.response = data.get(id=id)
            return Response({
                "response": self.response,
                "error": self.error
            })

        if params.get("address", None):
            data = data.filter(address=params.get("address"))
        if params.get("ids", None):
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

    def delete(self, request, warehouse_id=None):
        if warehouse_id:
            try:
                warehouse = Warehouse.objects.get(id=warehouse_id).delete()
                self.response = "Deleted succesfully"
            except Exception as e:
                self.error= True
                self.response= e.args[0]
        else:
            self.error = True
            self.response = "Only deletion by ID is supported"

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

    def delete(self, request, product_id=None):
        if product_id:
            try:
                product = Product.objects.get(id=product_id).delete()
                self.response = "Deleted succesfully"
            except Exception as e:
                self.error = True
                self.response = e.args[0]
        else:
            self.error = True
            self.response = "Only deletion by ID is supported"

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
        quantity = int(request.data.get("quantity"))
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
            if quantity + stock.available < 0:
                self.error = True
                self.response = "Not enough available stock"
            else:
                stock.available += quantity
                stock.save()
                order = Order.objects.create(date=datetime.now(),
                                             quantity=quantity,
                                             stock=stock)

                self.response = OrderSerializer(order, many=False).data

        return Response({
            "response": self.response,
            "error": self.error
        })


class DefaultWarehouseView(APIView):
    error = False
    response = ""

    def post(self, request):
        wh_id = request.data.get("warehouse")
        if not Warehouse.objects.filter(id=wh_id).exists():
            self.response = "Warehouse not found",
            self.error = True

        else:
            default_option, created = Meta.objects.get_or_create(option=DEFAULT_WH, defaults={"value": wh_id})
            if not created:
                default_option.value = wh_id
                default_option.save()

            self.response = "Warehouse {} set as default".format(str(wh_id))
            self.error = False

        return Response({
            "response": self.response,
            "error": self.error,
        })

    def get(self, request):
        try:
            default_option = Meta.objects.get(option=DEFAULT_WH)
            default_warehouse = Warehouse.objects.get(id=default_option.value)

            self.response = WarehouseSerializer(default_warehouse, many=False).data
            self.error = False
        except ObjectDoesNotExist:
            self.response = ""
            self.error = False

        return Response({
            "response": self.response,
            "error": self.error
        })

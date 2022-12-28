from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from manager_api.models import Warehouse, Product, Stock, Order
from manager_api.serializers import WarehouseSerializer


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

        self.response = data.all().WarehouseSerializer(data, many=True).data
        return Response({
            "response": self.response,
            "error": self.error
        })

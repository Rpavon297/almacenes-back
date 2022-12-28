from django.db import models
from datetime import datetime


class Warehouse(models.Model):
    address = models.CharField(max_length=255, null=False)


class Product(models.Model):
    name = models.CharField(max_length=30, null=False)


class Stock(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['warehouse', 'product'], name='stock_pk'
            )
        ]

    warehouse = models.OneToOneField(
        Warehouse,
        on_delete=models.CASCADE,
    )

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
    )

    available = models.IntegerField(null=False, default=0)


class Order(models.Model):
    stock = models.OneToOneField(
        Stock,
        on_delete=models.DO_NOTHING,
        primary_key=True
    )

    date = models.DateField(null=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    quantity = models.IntegerField(null=False)

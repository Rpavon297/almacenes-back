from django.db import models
from manager_api.constants import META_OPTIONS


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

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    available = models.IntegerField(null=False, default=0)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey(
        Stock,
        unique=False,
        on_delete=models.DO_NOTHING,
    )

    date = models.DateTimeField(null=False, default='28/12/2022 21:54:37')
    quantity = models.IntegerField(null=False)


class Meta(models.Model):
    # Here we store the default warehouse, instead of using a boolean in the warehouse table, to enforce only one wh
    # being the default and avoid having to filter/update the whole table to check/update the default one
    option = models.CharField(max_length=255, null=False, choices=META_OPTIONS)
    value = models.IntegerField(null=False)
